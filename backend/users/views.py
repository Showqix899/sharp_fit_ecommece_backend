from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer,UserSerializer


#permissions
from rest_framework.permissions import IsAuthenticated 
from .permissions import IsAdminUser #custom permission

#getting device info
from device_detector import DeviceDetector


#notification
from notifications.models import Notification
from notifications.tasks import send_notification_email

User = get_user_model()





# 🔹 1️⃣ User Registration View
class RegisterView(APIView):
    def post(self, request):

        #get meta data

        user_agent = request.META.get('HTTP_USER_AGENT','')

        #get device info
        device = DeviceDetector(user_agent).parse()
        device_type = device.device_type() or "unknown"  # e.g., 'desktop', 'mobile', 'tablet'
        device_name = device.device_brand() or "unknown" # e.g., 'Apple', 'Samsung', etc.
        device_model = device.device_model() or "unknown" # e.g., 'iPhone', 'Galaxy S21', etc.
        # device_info = {
        #     'device_type': device_type,
        #     'device_name': device_name,
        #     'device_model': device_model,
        # }

        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password'],
                default_device=device_model,
            
            )
            user.is_active = False  # User inactive until email verified
            user.save()

            domain = get_current_site(request).domain
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            activation_link = f'http://{domain}/api/activate/{uid}/{token}/'

            message = f"Hello {user.email},\n\n"
            message += "Click the link below to activate your account:\n\n"
            message += f"{activation_link}\n\n"
            message += "If you did not register, please ignore this email."
            message += f"\n\nDevice Info:\nType: {device_type}\nName: {device_name}\nModel: {device_model}"

            # Send email using Celery task
            subject = "Activate Your Account"
            send_notification_email.delay(
                user.email,
                subject,
                message,
            )
            
            


            return Response({'message': 'Check your email to activate your account!'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#admin registration view

class AdminRegisterView(APIView):
    def post(self, request):


        user_agent = request.META.get('HTTP_USER_AGENT','')

        #get device info
        device = DeviceDetector(user_agent).parse()
        device_type = device.device_type() or "unknown"  # e.g., 'desktop', 'mobile', 'tablet'
        device_name = device.device_brand() or "unknown"  # e.g., 'Apple', 'Samsung', etc.
        device_model = device.device_model() or "unknown" # e.g., 'iPhone', 'Galaxy S21', etc.



        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password'],
                role='ADMIN',
                default_device=device_model
            
            )
            user.is_active = False  # User inactive until email verified
            user.save()

            domain = get_current_site(request).domain
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            activation_link = f'http://{domain}/api/activate/{uid}/{token}/'

            message = f"Hello {user.email},\n\n"
            message += "Click the link below to activate your account:\n\n"
            message += f"{activation_link}\n\n"
            message += "If you did not register, please ignore this email."
            message += f"\n\nDevice Info:\nType: {device_type}\nName: {device_name}\nModel: {device_model}"


            # Send email using Celery task
            subject = "Activate Your Account as Admin"
            send_notification_email.delay(
                user.email,
                subject,
                message,
            )

            return Response({'message': 'Check your email to activate your account!'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 🔹 2️⃣ Account Activation View
class ActivateAccountView(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)

            if default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                return Response({'message': 'Account activated! You can now log in.','role':str(user.role)}, status=status.HTTP_200_OK)
            
            return Response({'message': 'Invalid activation link!'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({'message': 'Invalid activation link!'}, status=status.HTTP_400_BAD_REQUEST)


# 🔹 3️⃣ Login View
class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        
        user = User.objects.filter(email=email).first()
        

        if user and user.check_password(password):
            if not user.is_active:
                return Response({'message': 'Account is not activated!'}, status=status.HTTP_403_FORBIDDEN)

            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'role':user.role
            }, status=status.HTTP_200_OK)
        
        #get the current device info
        get_current_device = request.META.get('HTTP_USER_AGENT','')
        device = DeviceDetector(get_current_device).parse()
        current_device = device.device_model() or "unknown"  # e.g., 'iPhone', 'Galaxy S21', etc.

        if user and user.default_device != current_device:
            subject = "New Device Login Alert"
            message = f"Hello {user.email},\n\n"
            message += "A login attempt was made from a new device:\n\n"
            message += f"Device: {current_device}\n\n"
            message += "If this was you, please ignore this email. If not, please secure your account."
            send_notification_email.delay(
                email,
                subject,
                message,
            )
        

        # Update default device if it's the first login or missing
        if not user.default_device:
            user.default_device = current_device
            user.save()

        
        return Response({'message': 'Invalid credentials!'}, status=status.HTTP_401_UNAUTHORIZED)


# 🔹 4️⃣ Logout View
class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Logged out successfully!'}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'message': 'Invalid token!'}, status=status.HTTP_400_BAD_REQUEST)


# 🔹 5️⃣ Password Reset Request View
class PasswordResetView(APIView):
    def post(self, request):
        email = request.data.get("email")
        user = User.objects.filter(email=email).first()
        if user:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = f"http://127.0.0.1:8000/api/password-reset-confirm/{uid}/{token}/"

            message = f"Hello {user.email},\n\n"
            message += "Click the link below to reset your password:\n\n"
            message += f"{reset_link}\n\n"
            message += "If you did not request this, ignore this email."

            send_mail(
                "Password Reset Request",
                message,
                "no-reply@example.com",
                [user.email],
            )

            return Response({"message": "Password reset link sent!"}, status=status.HTTP_200_OK)
        
        return Response({"message": "Email not found!"}, status=status.HTTP_400_BAD_REQUEST)


# 🔹 6️⃣ Password Reset Confirm View
class PasswordResetConfirmView(APIView):
    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)

            if default_token_generator.check_token(user, token):
                password = request.data.get("password")
                password_confirm = request.data.get("password_confirm")

                if password != password_confirm:
                    return Response({"message": "Passwords do not match!"}, status=status.HTTP_400_BAD_REQUEST)

                user.set_password(password)
                user.save()

                return Response({"message": "Password reset successful!"}, status=status.HTTP_200_OK)
            return Response({"message": "Invalid or expired token!"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({"message": "Invalid reset link!"}, status=status.HTTP_400_BAD_REQUEST)



#user list view
class UserListView(APIView):
    permission_classes=[IsAuthenticated,IsAdminUser]

    def get(self,request):

        users = User.objects.all()

        serializer = UserSerializer(users, many =True)

        return Response(serializer.data,status=status.HTTP_200_OK)
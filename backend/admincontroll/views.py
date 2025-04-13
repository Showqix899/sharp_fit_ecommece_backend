from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q



# Create your views here.
#user

User=get_user_model() #custom user model
from users.permissions import IsAdminUser
from users.serializers import UserSerializer,AdminInvitation,AdminInviteSerializer

#activity log
from activity_log.models import ActivityLog


#product 
from products.models import Product,Color,Size
from products.serializers import ProductSerializer,ColorSerializer,SizeSerializer


#cart
from cart.models import Cart,CartItem
from cart.serializers import CartItemSerializer,CartSerializer,AddToCartSerializer,RemoveFromCartSerializer


#model
from orders.models import Order,OrderItem
from orders.serializers import OrderItemSerializer,OrderSerializer

#payments 
from payments.models import Payment

#notification
from notifications.models import Notification


#rest framework

from rest_framework.views import APIView
from rest_framework.generics import DestroyAPIView,UpdateAPIView,CreateAPIView,ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status






"""
Admin User View
"""
#update user
class AdminUserUpdateView(APIView):

    pemission_classes=[IsAuthenticated,IsAdminUser]
    serializer_class=UserSerializer

    def put(self,request):

        user_email=request.query_params.get('email')

        if not user_email:
            return Response({"error":"Please enter an email to delete the user"})
        
        try:
            user=User.objects.get(email=user_email)
            
        except User.DoesNotExist:
            return Response({"error":f"user not found with that email : {user_email}"})
        

        serializer=self.serializer_class(user,data=request.data,partial=True)

        if serializer.is_valid():

            serializer.save()
            return Response({"msg": "User updated successfully", "user": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
            


#destroy user
class AdminUserDeleteView(APIView):

    permission_classes=[IsAuthenticated,IsAdminUser]
    serializer_class=UserSerializer


    def delete(self,request):

        user_email=request.query_params.get('email')

        if not user_email:

            return Response({"error":"Please enter an email to delete the user"})

        

        try:
            user=User.objects.get(email=user_email)
            user.delete()
            return Response({"user":user.email,"msg":"user has been deleted"},status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"erro":f"can not find the user with that email {user_email}"},status=status.HTTP_404_NOT_FOUND)
        


#list of all admin
class ListOfAdmin(APIView):

    permission_classes=[IsAuthenticated,IsAdminUser]

    def get(self,request):
        try:

            users=User.objects.filter(role="ADMIN")
            serializer=UserSerializer(users,many=True)

            return Response(serializer.data,status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response ({"error":"currently no Admin found"},status=status.HTTP_204_NO_CONTENT)
        


#list of all user
class ListOfUsers(APIView):
    permission_classes=[IsAuthenticated,IsAdminUser]

    def get(self,request):
        try:

            users=User.objects.filter(role="USER")
            serializer=UserSerializer(users,many=True)

            return Response(serializer.data,status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response ({"error":"currently no user found"},status=status.HTTP_204_NO_CONTENT)


#retrive user details
class UserDetailsView(APIView):

    permission_classes=[IsAuthenticated,IsAdminUser]
    def get(self,request):

        user_email=request.query_params.get('email')
        
        if not user_email:

            return Response({"error":"Please enter an email to delete the user"})
        
        try:
            user=User.objects.get(email=user_email)

        except User.DoesNotExist:
            return Response({"erro":f"can not find the user with that email {user_email}"},status=status.HTTP_404_NOT_FOUND)
        

        serializer=UserSerializer(user)
        return Response({"msg": "User list", "user": serializer.data})




#admin invite view 
#for generating an invitation link
@api_view(['POST'])
@permission_classes([IsAuthenticated,IsAdminUser])
def generate_admin_invite(request):

    expiry=timezone.now()+timezone.timedelta(hours=2)
    invite = AdminInvitation.objects.create(
        created_by=request.user,
        expires_at=expiry
    )
    link = f'http://{get_current_site(request).domain}/api/admin/register/?token={invite.token}'
    return Response({"invite_link":link},status=201)






"""
Admin product view
"""

#update product
class UpdateProductView(APIView):

    permission_classes=[IsAuthenticated,IsAdminUser]

    def put(self,request):

       #get the filter values 
        name = request.query_params.get('name')
        description = request.query_params.get('description')
        category = request.query_params.get('category')
        color = request.query_params.get('color')
        size = request.query_params.get('size')

        name = name.lower() if name else None
        description=description.lower() if description else None
        print(name)

        filters=Q()
        if name:
            filters &= Q(name__icontains=name)
        if description:
            filters &= Q(description__icontains=description)
        if category:
            filters &= Q(category__iexact=category)
        if color:
            filters &= Q(colors__name__iexact=color)
        if size:
            filters &= Q(sizes__name__iexact=size)

        #search product
        product = Product.objects.filter(filters).distinct().first()
        
        if not product:

            return Response({"error":"No matching product found"},status=status.HTTP_404_NOT_FOUND)
        

        serializer=ProductSerializer(product,data=request.data,partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response({"product":serializer.data,"msg":"product updated successfully"},status=status.HTTP_200_OK)

        return Response({"error":serializer.errors,'msg':"something went wrong"})
    


#update product
class DeleteProductView(APIView):

    permission_classes=[IsAuthenticated,IsAdminUser]

    def delete(self,request):

       #get the filter values 
        name = request.query_params.get('name')
        description = request.query_params.get('description')
        category = request.query_params.get('category')
        color = request.query_params.get('color')
        size = request.query_params.get('size')

        name = name.lower() if name else None
        description=description.lower() if description else None
        print(name)

        filters=Q()
        if name:
            filters &= Q(name__icontains=name)
        if description:
            filters &= Q(description__icontains=description)
        if category:
            filters &= Q(category__iexact=category)
        if color:
            filters &= Q(colors__name__iexact=color)
        if size:
            filters &= Q(sizes__name__iexact=size)

        #search product
        product = Product.objects.filter(filters).distinct().first()
        
        if not product:

            return Response({"error":"No matching product found"},status=status.HTTP_404_NOT_FOUND)
        
        product.delete()

        return Response({"product":f"{name}","msg":"product deleted successfully"},status=status.HTTP_200_OK)



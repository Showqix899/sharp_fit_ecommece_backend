from django.shortcuts import render

# Create your views here.
from .models import ActivityLog

from django.http import JsonResponse

from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt

class list_log(APIView):
    permission_classes = [AllowAny]
    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return super().get_permissions()
    def get(self, request):
        # Assuming you want to return all logs
        logs = ActivityLog.objects.all()
        
        return JsonResponse({"logs": [log.action for log in logs]})
    
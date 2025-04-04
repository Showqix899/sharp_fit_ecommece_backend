from django.db import models
from django.contrib.auth import get_user_model



# Create your models here.
User = get_user_model()

#activity log model

class ActivityLog(models.Model):

    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="activity_logs",null=True,blank=True)
    action=models.CharField(max_length=255,null=True,blank=True)
    timestamp=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    details=models.JSONField(null=True,blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.timestamp}"
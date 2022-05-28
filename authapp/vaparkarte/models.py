from django.db import models
from django.contrib.auth.models import User

from vaparkarte.views import forgot_pass

class Profile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    forgot_pass_token=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)

def __str__(self):
    return self.user.username 

from django.db import models
from user.models import User
from django.db import models
from django.conf import settings
"""
transactions model
"""
class TransferMoney(models.Model):
    
    sender = models.ForeignKey(User, on_delete=models.CASCADE,related_name='sender')
    receiver  = models.ForeignKey(User, on_delete=models.CASCADE,related_name='receiver')
    datetime = models.DateTimeField()
    is_approved = models.CharField(default='0', max_length=1)
    amount = models.IntegerField()
    
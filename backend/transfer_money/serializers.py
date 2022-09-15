from rest_framework import serializers
from transfer_money.models import TransferMoney
from user.models import User
from user import jwt
from datetime import datetime, timedelta
from django.conf import settings

"""
Serializer fields handle converting between primitive values 
and internal datatypes.
They also deal with validating input values,
as well as retrieving 
and setting the values from their parent objects.
"""
# transaction serializer
class TransactionSerializer(serializers.ModelSerializer):
    class Meta():
        model = TransferMoney
        fields=(
            'sender',
            'receiver',
            'amount',
            'datetime',
            'is_approved',
        )
    def is_valid(self, raise_exception=False):
        return super().is_valid(raise_exception)

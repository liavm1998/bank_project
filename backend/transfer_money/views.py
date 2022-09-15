from transfer_money.models import TransferMoney
from user.models import User
from .serializers import TransactionSerializer
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from user.serializers import UserSerializer
from datetime import datetime



class TransactionListView(GenericAPIView):
    """
    http://127.0.0.1:8000/api/transactions/
    """
    serializer_class = TransactionSerializer
    queryset = TransferMoney.objects.all()
    def get(self,*args, **kwargs):
        data = []
        for t in self.queryset.all():
            t_data = {}
            t_data['id'] = t.id

            from_data = UserSerializer(User.objects.get(id=t.sender.id)).data
            from_data.pop('token')
            t_data['from'] = from_data

            to_data = UserSerializer(User.objects.get(id=t.receiver.id)).data
            to_data.pop('token')
            t_data['to'] = to_data
            t_data['amount'] = t.amount
            t_data['datetime'] = t.datetime
            t_data['is_approved'] = False
            if t.is_approved == 't':
                t_data['is_approved'] = True
            data.append(t_data)
        return Response(data)


class RejectTransactionView(GenericAPIView):
    """
    http://127.0.0.1:8000/api/transaction/<id>/reject/
    """
    def post(self,request,id,*args, **kwargs):
        transaction = TransferMoney.objects.get(id=id) # get transaction details
        if transaction.is_approved != '0':
            return Response({"fail": "transaction already approved or rejected"})    
        receiver_id = transaction.receiver.id # get target details
        # only if the current user is transaction target user
        if request.user.id != receiver_id:
            return Response({"fail": "this user is not the transaction target user"})    
        receiver = User.objects.get(id=receiver_id)
        transaction.is_approved = 'f'
        transaction.save()
        return Response({"succees": True})    


class AcceptTransactionView(GenericAPIView):
    """
    http://127.0.0.1:8000/api/transaction/<id>/accept/
    """
    serializer_class = TransactionSerializer
    def post(self,request,id,*args, **kwargs):
        
        transaction = TransferMoney.objects.get(id=id) # get transaction details
        if transaction.is_approved != '0':
            return Response({"succeed": False},status=400)    
        receiver_id = transaction.receiver.id # get target details
        # only if the current user is transaction target user
        if request.user.id != receiver_id:
            return Response({"succeed": False})    
        receiver = User.objects.get(id=receiver_id)

        # get sender details
        sender_id = transaction.sender.id
        sender = User.objects.get(id=sender_id)
        
        # check if sender has the money
        if int(sender.user_balance)<int(transaction.amount):
            return Response({"succeed": False})    
        
        # make the transaction
        sender.user_balance = sender.user_balance -  int(transaction.amount)
        receiver.user_balance = receiver.user_balance +  int(transaction.amount)
        transaction.is_approved = 't'

        # save the transaction
        sender.save()
        receiver.save()
        transaction.save()
        
        return Response({"succeed": True})


class CreateTransactionView(GenericAPIView):
    """
    http://127.0.0.1:8000/api/send_money/
    """
    serializer_class = TransactionSerializer    
    def post(self,request,*args, **kwargs):
        data = request.data
        data['datetime'] = datetime.now()
        data['sender'] = request.user.id
        data['is_approved'] = '0'
        try:
            data['receiver'] = User.objects.filter(username=data['user'])[0].id
        except:
            try:
                data['receiver'] = User.objects.filter(email=data['email'])[0].id
            except:
                return Response({"error": "trying to send money to non-registered user"},status=400)        
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid() and request.user.user_balance>=data['amount']:
            serializer.save()
            return Response({"succeed": True},status=201)
        return Response({"succeed": False},status=400)

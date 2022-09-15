from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import permissions
from transfer_money.models import TransferMoney
from user.models import User
from transfer_money import views as transaction_views
from user import views as user_views 

"""
this script destinition 
is to import all the models related views tp the main app (api)
"""
# User Views
RegisterView = user_views.ReigsterAPIView.as_view()
LoginView = user_views.LoginAPIView.as_view()
ProfileView = user_views.AuthUserProfile.as_view()
InviteView = user_views.InviteFriendView.as_view()
# Transaction Views
SendView = transaction_views.CreateTransactionView.as_view()
AcceptView =  transaction_views.AcceptTransactionView.as_view()
RejectView = transaction_views.RejectTransactionView.as_view()
TransactionsView = transaction_views.TransactionListView.as_view()
# admin view
class StatisticsAPIView(GenericAPIView):
    permission_classes = [permissions.IsAdminUser]
    def get(self,*args, **kwargs):
        data = {}
        data['total_money_transferred'] = 0
        data['amount_users'] = User.objects.count()
        data['amount_transaction'] = TransferMoney.objects.all().count()
        data['amount_transaction_accepted'] = TransferMoney.objects.filter(is_approved='t').count()
        data['amount_transaction_rejected'] = TransferMoney.objects.filter(is_approved='f').count()
        
        
        qs = TransferMoney.objects.filter(is_approved='t')
        for t in qs.all():
            data['total_money_transferred'] += t.amount
        return Response(data)

# just sticking to the convention of making views object
StatisticsView = StatisticsAPIView.as_view()


    

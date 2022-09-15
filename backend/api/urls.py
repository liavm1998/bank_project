from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.RegisterView,name='register'),
    path('login/',views.LoginView,name='login'),
    path('profile/',views.ProfileView,name='profile'),
    path('invite_friend/',views.InviteView,name='invite_friend'),
    path('send_money/',views.SendView,name='send_money'),
    path('transaction/<int:id>/accept/',views.AcceptView,name='accept_money'),
    path('transaction/<int:id>/reject/',views.RejectView,name='reject_money'),
    path('transactions/',views.TransactionsView,name='transactions_list'),
    path('statistics/',views.StatisticsView,name='statistics'),
]

from .serializers import UserSerializer, LoginSerializer, ProfileSerializer
from rest_framework.generics import GenericAPIView
from rest_framework import status,permissions
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .models import User
from .mail_sender import send_mail_to


class ReigsterAPIView(GenericAPIView):
    """
    https://localhost:8000/api/register/
    """
    authentication_classes = []
    serializer_class = UserSerializer
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if  serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class InviteFriendView(GenericAPIView):
    """
    https://localhost:8000/api/invite_friend/
    """
    permission_classes = (permissions.IsAuthenticated,)
    
    def post(self,request):
        receiver = request.data.get('email')
        try:
            User.objects.get(email=receiver)
            return Response({'succeed':'False'},status=status.HTTP_400_BAD_REQUEST)
        except:
            send_mail_to(receiver)
            return Response({'succeed':'True'},status=status.HTTP_202_ACCEPTED)
            
            


class AuthUserProfile(GenericAPIView):
    """
    https://localhost:8000/api/profile/
    """
    def get(self,request):
        user = request.user
        instance = ProfileSerializer(user)
        return Response(instance.data)
    

class LoginAPIView(GenericAPIView):
    """
    https://localhost:8000/api/login/
    """
    authentication_classes = []
    serializer_class = LoginSerializer
    def post(self,request):
        # always needed info
        password=request.data.get('password')
        
        username = request.data.get('username')
        # may be None
        if username:
            # uf username not None try authenticate using username and email
            user = authenticate(username=username,password=password)
        else:
            #if None try authenticate using email and password
            email = request.data.get('email')
            try:
                # check if accepted email exist in the database and take username out of it
                username = User.objects.get(email=email).username
                user = authenticate(username=username,password=password)
            except:

                return Response({'error':'username with the accepted email doesn\'t exists'},status=status.HTTP_401_UNAUTHORIZED)            
        if user:
            # if we got here that mean we already authentificated
            serializer = self.serializer_class(user)
            return Response({'token':serializer.data.get('token')},status=status.HTTP_200_OK)
        return Response({'error':'invalid username or password'},status=status.HTTP_401_UNAUTHORIZED)

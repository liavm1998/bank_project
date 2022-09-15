from rest_framework.authentication import get_authorization_header,BaseAuthentication
from rest_framework import exceptions
from django.conf import settings
from .models import User
import jwt

class JWTAuthentification(BaseAuthentication):
    """
    my own token authenticate based on my understanding of the original
    """

    def authenticate(self, request):
        auth_header = get_authorization_header(request)
        auth_data = auth_header.decode('utf-8')
        auth_token = auth_data.split(" ")

        if len(auth_token) != 2:
            raise exceptions.AuthenticationFailed
        token = auth_token[1]
        try:
            """
            HS256 is a symmetric algorithm that shares one secret key between 
            the identity provider and your application.
            """
            payload = jwt.decode(token,settings.SECRET_KEY,algorithms='HS256')
            try: 
                username = payload['username']
                user = User.objects.get(username=username)
            except:
                email = payload['email']
                user = User.objects.get(email=email)    
            return (user,token)

        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token has expired, login again')
        except jwt.DecodeError:
            raise exceptions.AuthenticationFailed('Token is invalid')
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('User does not exist')
        
from rest_framework.views import APIView
from rest_framework.permissions import  AllowAny, IsAuthenticated
from .serializer import RegisterSerializer, LoginSerializer, PasswordResetSerializer, passwordConfirmSerializer
from rest_framework.response import Response
from rest_framework import status
from auth_app.utils import encode_uid, account_activation_token, get_user_from_uidb64
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import (TokenRefreshView)
from auth_app.models import CustomUser
from auth_app.tasks import send_activation_email, send_password_reset_mail
from django.contrib.auth.tokens import default_token_generator


class RegisterView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            account = serializer.save()
            uid = encode_uid(account)
            token = account_activation_token.make_token(account)
            send_activation_email(account, uid, token)

        else:
            return Response(serializer.errors, status=400)
        return Response({"user": serializer.data, "token": token}, status=201)

class ActivateTokenView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        user = get_user_from_uidb64(uidb64)
        if user is None:
            return Response({'error': 'Account does not exist.'}, status=400)
        
        valid = account_activation_token.check_token(user, token)
        
        if user.is_active:
            return Response({'error': 'Account already activated.'}, status=400)
        
        if valid:
            user.is_active = True
            user.save()
            return Response({"message": "Account successfully activated."}, status=200)
        return Response({"message": "Account not activated!."}, status=400)

class LoginView(APIView):

    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            token = RefreshToken.for_user(user)
            refresh_token = str(token)
            access_token = str(token.access_token)

            response = Response({'detail': '"Login successful', 'user': {'id':user.id, 'username': user.email}} ,status=200)
            response.set_cookie('refresh_token', refresh_token, httponly=True)
            response.set_cookie('access_token', access_token, httponly=True)
            return response
        else:
            return Response(serializer.errors, status=401)

class LogoutView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        refresh = request.COOKIES.get('refresh_token')
        if refresh is None:
            return Response({'detail': 'Refresh token is missing.'}, status=400)

        try:
            token = RefreshToken(refresh)
            token.blacklist()
        except:
            return Response({'detail': 'Refresh token is invalid.'}, status=400)

        response = Response({"detail": "Logout successful! All tokens will be deleted. Refresh token is now invalid."}, status=200)
        response.delete_cookie("access_token")
        response.delete_cookie('refresh_token')
        return response

class RefreshCookieView(TokenRefreshView):
    def post(self, request):

        refresh = request.COOKIES.get('refresh_token')

        if refresh is None:
            return Response({'detail':'Refresh token is missing.'}, status=400)
        request.data['refresh'] = refresh
        try:
            access = super().post(request)
        except:
            return Response({'detail': 'Refresh token is invalid.'}, status=401)
        access_token = access.data['access']

        response = Response({'detail': 'Token refreshed', 'access': access_token}, status=200)
        response.set_cookie('access_token', access_token, httponly=True)
        return response

class PasswordResetView(APIView):

    def post(self, request):
        data = request.data
        serializer = PasswordResetSerializer(data=data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = CustomUser.objects.filter(email=email).first()
            if user is not None:
                uid = encode_uid(user)
                token = default_token_generator.make_token(user)
                send_password_reset_mail(user, uid, token)
            response = Response({'detail': 'An email has been sent to reset your password.'}, status=200)
            return response
        return Response({'detail': 'Invalid Email.'}, status=400)

class PasswordConfirmView(APIView):
    def post (self, request, uidb64, token):

        user = get_user_from_uidb64(uidb64)
        if user is None:
            return Response({'error': 'Account does not exist.'}, status=400)

        valid = default_token_generator.check_token(user, token)
        if not valid:
            return Response({'error': 'Token is invalid.'}, status=400)

        data = request.data
        serializer = passwordConfirmSerializer(data=data)

        if serializer.is_valid():
            new_password = serializer.validated_data['new_password']
            user.set_password(new_password)
            user.save()
            return Response({'detail': 'Your Password has been successfully reset.'}, status=200)
        return Response({'error': 'password dont match.'}, status=400)
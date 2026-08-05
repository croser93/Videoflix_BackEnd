from rest_framework.views import APIView
from rest_framework.permissions import  AllowAny, IsAuthenticated
from .serializer import RegisterSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework import status
from auth_app.utils import encode_uid, account_activation_token, get_user_from_uidb64
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import (TokenRefreshView)


class RegisterView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            account = serializer.save()
            uid = encode_uid(account)
            token = account_activation_token.make_token(account)

        else:
            return Response(serializer.errors, status=400)
        return Response ({"user": serializer.data}, status=201)

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

            response = Response({'detail': 'Login successfully!', 'user': {'id':user.id, 'username': user.email}} ,status=200)
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
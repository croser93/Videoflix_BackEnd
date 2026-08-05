from rest_framework.views import APIView
from rest_framework.permissions import  AllowAny
from .serializer import RegisterSerializer
from rest_framework.response import Response
from rest_framework import status
from auth_app.utils import encode_uid, account_activation_token



class RegisterView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
           account = serializer.save()
           uid = encode_uid(account)
           token = account_activation_token.make_token(account)
           print(uid, token)
        else:
            return Response(serializer.errors, status=400)
        return Response ({"user": serializer.data}, status=201)


class LoginView(APIView):
    pass

class LogoutView(APIView):
    pass
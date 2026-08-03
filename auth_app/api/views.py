from rest_framework.views import APIView
from rest_framework.permissions import  AllowAny
from .serializer import RegisterSerializer
from rest_framework.response import Response
from rest_framework import status


class RegisterView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            print("erfolgreich erstellt")
        else:
            return Response(serializer.errors, status=400)
        return Response ({"detail": "User created successfully!"}, status=201)


class LoginView(APIView):
    pass

class LogoutView(APIView):
    pass
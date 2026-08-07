from rest_framework import serializers
from auth_app.models import CustomUser
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):

    confirmed_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password', 'confirmed_password']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True, 'validators': []}
        }

    def save(self, **kwargs):
        email = self.validated_data['email']
        pw = self.validated_data['password']
        confirmed_password = self.validated_data['confirmed_password']

        all_emails = CustomUser.objects.filter(email=email).exists()

        if pw != confirmed_password:
            raise serializers.ValidationError({'error': 'password dont match' })
        
        if all_emails:
            raise serializers.ValidationError({'error' : 'email exist'})
        
        account = CustomUser.objects.create_user(email=email, password=pw)
        self.instance = account
        return account

class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])

        if user:
            return{'user': user}
        else:
            raise serializers.ValidationError({'error': 'wrong credentials'})
    

class PasswordResetSerializer(serializers.Serializer):

    email = serializers.EmailField(write_only=True)

class passwordConfirmSerializer(serializers.Serializer):

    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)


    def validate(self, data):
        if data['new_password'] == data['confirm_password']:
            return data
        raise serializers.ValidationError({'error': 'passwords dont match.'})


from rest_framework import serializers
from django.contrib.auth.models import User

class RegisterSerializer(serializers.ModelSerializer):

    confirmed_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'confirmed_password']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}
        }

    def save(self, **kwargs):
        email = self.validated_data['email']
        pw = self.validated_data['password']
        confirmed_password = self.validated_data['confirmed_password']

        all_emails = User.objects.filter(email=email).exists()

        if pw != confirmed_password:
            raise serializers.ValidationError({'error': 'password dont match' })
        
        if all_emails:
            raise serializers.ValidationError({'error' : 'email exist'})
        
        account = User (
            email = email
        )

        account.set_password(pw)
        account.save()
        return account
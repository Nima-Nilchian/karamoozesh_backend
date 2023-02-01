from django.contrib.auth import authenticate
from rest_framework import serializers
from user.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'error': 'p1 and p2 should be same!'})

        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({'error': 'Email Already exists!'})

        account = User(email=self.validated_data['email'], username=self.validated_data['username'])
        account.set_password(password)
        account.save()

        return account


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(style={'input_type': 'email'}, write_only=True)
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    def validate(self, attrs):
        email = attrs['email']
        password = attrs['password']

        if email and password:
            user = authenticate(request=self.context.get('request'), username=email, password=password)
            if not user:
                msg = 'user is not registered'
                raise serializers.ValidationError(msg, code='authorization')

        else:
            msg = 'Must include email and password'
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs



class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        fields = ("email",)



class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True, min_length=1)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True, min_length=1)

    class Meta:
        field = ("password", "password2")

    def validate(self, attrs):

        # Verify token and encoded_pk and then set new password.
        password = attrs.get("password")
        password2 = attrs.get("password2")

        token = self.context.get("kwargs").get("token")
        encoded_pk = self.context.get("kwargs").get("encoded_pk")

        if token is None or encoded_pk is None:
            raise serializers.ValidationError("Missing data.")

        pk = urlsafe_base64_decode(encoded_pk).decode()
        user = User.objects.get(pk=pk)
        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError("The reset token is invalid")

        if password != password2:
            raise serializers.ValidationError({'error': 'pass1 and pass2 should be same!'})

        user.set_password(password)
        user.save()
        return attrs






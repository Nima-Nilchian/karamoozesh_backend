from django.contrib.auth import authenticate
from .models import User, Profile
from rest_framework import serializers


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


class ChangePasswordSerializer(serializers.Serializer):
    model = User
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email']


class ProfileSettingSerializer(serializers.ModelSerializer):
    user = UserSerializer(source='user_id', read_only=True)
    first_name = serializers.CharField(max_length=150, write_only=True)
    last_name = serializers.CharField(max_length=150, write_only=True)
    username = serializers.CharField(max_length=20, write_only=True)

    class Meta:
        model = Profile
        fields = ['image', 'phone_number', 'user', 'first_name', 'last_name', 'username']

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        user = self.context['request'].user

        if 'first_name' in validated_data:
            user.first_name = validated_data['first_name']
        if 'last_name' in validated_data:
            user.last_name = validated_data['last_name']
        if 'username' in validated_data:
            user.username = validated_data['username']
        user.save()
        return instance


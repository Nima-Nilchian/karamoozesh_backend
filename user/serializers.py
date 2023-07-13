from django.contrib.auth import authenticate
from cv.models import CV
from ticket.models import Ticket
from .models import User, Profile, FavoriteCVs
from rest_framework import serializers


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


class FavoriteCVsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteCVs
        fields = ['cv_id']


class ProfileActivitySerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    favorite_cvs = serializers.HyperlinkedRelatedField(view_name='resume_detail', source='favorite_cv', many=True, read_only=True)
    cv = serializers.HyperlinkedIdentityField(view_name='resume_detail')

    class Meta:
        model = User
        fields = ['user', 'favorite_cvs', 'cv']

    def get_user(self, obj):
        return UserSerializer(obj, read_only=True).data

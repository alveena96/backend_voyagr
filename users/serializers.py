from rest_framework import serializers
from .models import CustomUser
import json

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    location = serializers.ListField(
        child=serializers.FloatField(), write_only=True
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'location']

    def create(self, validated_data):
        location = validated_data.pop('location')
        
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email'),
            location=json.dumps(location)  # store as string
        )
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id',
            'username',
            'mobile_number',
            'email',
            'picture',
            'is_active',
            'is_staff',
            'created_at',
            'user_creator',
        ]
        read_only_fields = fields

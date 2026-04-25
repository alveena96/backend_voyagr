from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import *
from django.shortcuts import get_object_or_404
from .models import CustomUser
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView



class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)



class UsersListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.query_params.get('user')

        # If a specific user ID is requested
        if user_id:
            # Only admin can fetch other users
            if not request.user.is_staff:
                return Response({"error": "Not allowed"}, status=403)

            user = get_object_or_404(CustomUser, id=user_id)
            serializer = UserProfileSerializer(user)
            return Response(serializer.data)

        # No user param → list users
        # Admin sees all, normal user sees only themselves
        if request.user.is_staff:
            users = CustomUser.objects.all()
        else:
            users = CustomUser.objects.filter(id=request.user.id)

        serializer = UserProfileSerializer(users, many=True)
        return Response(serializer.data)
    


class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "User created successfully"
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        if not CustomUser.objects.filter(id=user.id).exists():
            raise serializers.ValidationError("User does not exist.")

        data['user_id'] = user.id
        data['user_name'] = user.username

        return data


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        return super().validate(attrs)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer


class TokenVerificationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(True)
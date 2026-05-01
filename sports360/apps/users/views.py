from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from apps.users.models import User, EmailVerification
from apps.users.serializers import (
    UserSerializer, RegisterSerializer, LoginSerializer,
    AdminRegisterSerializer, SendVerificationCodeSerializer, VerifyEmailSerializer
)
from apps.users.email_service import send_verification_email, verify_email_code
from apps.users.permissions import IsAdmin


class RegisterView(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Send verification email
            success, message = send_verification_email(user)
            if not success:
                return Response(
                    {
                        'message': 'User registered successfully',
                        'warning': message,
                        'user': UserSerializer(user).data,
                        'email_sent': False
                    },
                    status=status.HTTP_201_CREATED
                )

            return Response(
                {
                    'message': 'User registered successfully. Verification code sent to email.',
                    'user': UserSerializer(user).data,
                    'email_sent': True,
                    'next_step': 'Verify your email with the code sent to ' + user.email
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminRegisterView(viewsets.ViewSet):
    permission_classes = [IsAdmin]

    def create(self, request):
        """Only admins can create other admins"""
        serializer = AdminRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    'message': 'Admin created successfully',
                    'user': UserSerializer(user).data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            tokens = serializer.create(serializer.validated_data)
            return Response(tokens, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendVerificationCodeView(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def create(self, request):
        """Send verification code to email"""
        serializer = SendVerificationCodeSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)

            success, message = send_verification_email(user)

            if success:
                return Response(
                    {
                        'message': message,
                        'email': email,
                        'code_sent': True
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'message': message},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailView(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def create(self, request):
        """Verify email with code"""
        serializer = VerifyEmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            code = serializer.validated_data['code']

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response(
                    {'message': 'User not found'},
                    status=status.HTTP_404_NOT_FOUND
                )

            success, message = verify_email_code(user, code)

            if success:
                return Response(
                    {
                        'message': message,
                        'user': UserSerializer(user).data,
                        'verified': True
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'message': message},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def retrieve(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def update(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


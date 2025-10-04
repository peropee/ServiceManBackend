from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from .models import ClientProfile, ServicemanProfile
from .serializers import (
    UserSerializer, RegisterSerializer,
    ClientProfileSerializer, ServicemanProfileSerializer
)
from .tokens import email_verification_token

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        if user.user_type == 'CLIENT':
            ClientProfile.objects.create(user=user)
        elif user.user_type == 'SERVICEMAN':
            ServicemanProfile.objects.create(user=user)
        # Send verification email
        self.send_verification_email(user)

    def send_verification_email(self, user):
        token = email_verification_token.make_token(user)
        uid = user.pk
        url = self.request.build_absolute_uri(
            reverse('users:verify-email') + f"?uid={uid}&token={token}"
        )
        send_mail(
            "Verify your email",
            f"Please verify your email: {url}",
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
        )

class VerifyEmailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        uid = request.GET.get('uid')
        token = request.GET.get('token')
        user = get_object_or_404(User, pk=uid)
        if email_verification_token.check_token(user, token):
            user.is_email_verified = True
            user.save()
            return Response({"detail": "Email verified."}, status=200)
        return Response({"detail": "Invalid token."}, status=400)

class UserMeView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class ClientProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ClientProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.client_profile

class ServicemanProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ServicemanProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.serviceman_profile

class PasswordResetRequestView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        email = request.data.get('email')
        user = get_object_or_404(User, email=email)
        token = default_token_generator.make_token(user)
        uid = user.pk
        url = self.request.build_absolute_uri(
            reverse('users:password-reset-confirm') + f"?uid={uid}&token={token}"
        )
        send_mail(
            "Password Reset",
            f"Use this link to reset your password: {url}",
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
        )
        return Response({"detail": "Password reset email sent."})

class PasswordResetConfirmView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        uid = request.GET.get('uid')
        token = request.GET.get('token')
        password = request.data.get('password')
        user = get_object_or_404(User, pk=uid)
        if default_token_generator.check_token(user, token):
            user.set_password(password)
            user.save()
            return Response({"detail": "Password has been reset."})
        return Response({"detail": "Invalid token."}, status=400)
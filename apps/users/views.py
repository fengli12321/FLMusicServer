from datetime import datetime
from random import choice

from rest_framework import mixins
from rest_framework import viewsets, views
from rest_framework.response import Response
from rest_framework import status
from rest_framework_jwt.views import jwt_response_payload_handler, JSONWebTokenAPIView
from rest_framework_jwt.settings import api_settings


from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from .serializers import LoginSerializer

from .models import VerifyCode
from .serializers import VerifyCodeSerializer, UserRegSerializer

User = get_user_model()
class CustomBackend(ModelBackend):
    """
    自定义用户验证
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username)|Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LoginView(JSONWebTokenAPIView):
    serializer_class = LoginSerializer
    def post(self, request, formate=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.object.get('user') or request.user
        token = serializer.object.get('token')
        response_data = jwt_response_payload_handler(token, user, request)
        response = Response(response_data)
        if api_settings.JWT_AUTH_COOKIE:
            expiration = (datetime.utcnow() +
                          api_settings.JWT_EXPIRATION_DELTA)
            response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                token,
                                expires=expiration,
                                httponly=True)
        return response


class VerifyCodeViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = VerifyCode.objects.all()
    serializer_class = VerifyCodeSerializer

    def generate_code(self):
        seeds = "0123456789"
        random_str = []
        for i in range(6):
            random_str.append(choice(seeds))
        return "".join(random_str)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = self.generate_code()
        verify_code = VerifyCode(code=code, mobile=serializer.data["mobile"])
        verify_code.save()
        headers = self.get_success_headers(serializer.data)
        return Response({"code": code}, status=status.HTTP_201_CREATED, headers=headers)




class UserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegSerializer

    def perform_create(self, serializer):
        return serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        user.set_password(user.password)
        user.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



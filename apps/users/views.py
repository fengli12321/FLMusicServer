from django.shortcuts import render
from random import choice

from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework_jwt.serializers import jwt_payload_handler

from .models import VerifyCode
from .serializers import VerifyCodeSerializer, UserRegSerializer


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
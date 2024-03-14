
import re
from rest_framework import viewsets
from .models import NUser
from .serializers import NUserSerializer
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password,check_password
# from django.contrib.auth import authenticate

class NUserViewSet(viewsets.ModelViewSet):
    queryset = NUser.objects.all()
    serializer_class = NUserSerializer

    def register(self,request):
        username=request.data.get('username')
        password=request.data.get('password')
        encrypt_pwd=make_password(password)
        email=request.data.get('email')
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            msg = '邮箱错误'
            return Response(data={"detail": "邮箱格式错误"}, status=404)
        users=NUser.objects.create(username=username,password=encrypt_pwd,email=email)
        users.save()
        return Response(data={"detail":"success"})

    def login(self,request):
        username = request.data.get('username')
        password = request.data.get('password')
        queryset=NUser.objects.get(username=username)
        encrypt_pwd=queryset.password
        users=check_password(password,encrypt_pwd)
        if not users:
            return Response(data={"detail": " 用户名或密码不正确 "}, status=404)
        return Response(data={"detail":"success"})


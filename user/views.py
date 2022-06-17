from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response

from django.contrib.auth import login, logout, authenticate


# APIView를 상속 받아 이제 Rest Framework의 APIView 가 됨
class UserView(APIView):    # CVB 방식

    permission_classes = [permissions.AllowAny]  # 누구나 view 조회 가능
    # permission_classes = [permissions.IsAdminUser]  # admin만 view 조회 가능
    # permission_classes = [permissions.IsAuthenticated] # 로그인 된 사용자만 view 조회 가능

    def get(self, request):     # 사용자 정보 조회
        return Response({"message": "get method! success"})

    def post(self, request):    # 회원가입
        return Response({"message": "post method! success"})

    def put(self, request):     # 회원 정보 수정
        return Response({"message": "put method! success"})

    def delete(self, request):  # 회원 탈퇴
        return Response({"message": "delete method! success"})


class UserAPIView(APIView):
    permission_classes = [permissions.AllowAny]  # 누구나 view 조회 가능

    # 로그인
    def post(self, request):
        username = request.data.get('username', '')
        password = request.data.get('password', '')

        user = authenticate(request, username=username, password=password)

        if not user:
            return Response({"error": "존재하지 않는 계정이거나 패스워드가 일치하지 않습니다."})

        login(request, user)
        return Response({"message": "login success!!"})

    def delete(self, request):
        logout(request)
        return Response({"message": "logout success!!"})

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from django.db.models import F, Q

from django.contrib.auth import login, logout, authenticate

from user.models import UserProfile

from user.serializers import UserSerializer     # 시리얼라이즈를 가져 옴

from user.models import UserProfile as UserProfileModel
from user.models import User as UserModel
from user.models import Hobby as HobbyModel


# APIView를 상속 받아 이제 Rest Framework의 APIView 가 됨
class UserView(APIView):    # CVB 방식

    permission_classes = [permissions.AllowAny]  # 누구나 view 조회 가능
    # permission_classes = [permissions.IsAdminUser]  # admin만 view 조회 가능
    # permission_classes = [permissions.IsAuthenticated] # 로그인 된 사용자만 view 조회 가능

    def get(self, request):     # 사용자 정보 조회
        
        all_users = UserModel.objects.all()
        
        return Response(UserSerializer(all_users, many=True).data)  # 뒤에 data를 붙여줘야 결과물이 json으로 return 됨

        # OneToOne field는 예외로 _set이 붙지 않는다.
        # hobbys = user.userprofile.hobby.all()    # 역참조 사용

        # for hobby in hobbys:
        #     '''
        #     exclde : 매칭 된 쿼리만 제외, filter와 반대
        #     annotate : 필드 이름을 변경해주기 위해 사용, 이외에도 원하는 필드를 추가하는 등 다양하게 활용 가능
        #     values / values_list : 지정한 필드만 리턴 할 수 있음. values는 dict로 return, values_list는 tuple로 ruturn
        #     F() : 객체에 해당되는 쿼리를 생성함
        #     annotate : field의 이름을 바꿔서 추력해주거나
        #         새로운 field를 추가해주고 싶을 때 sum
        #     '''
        #     hobby_members = hobby.userprofile_set.exclude(user=user).annotate(username=F('user__username')).values_list('username', flat=True)
        #     hobby_members = list(hobby_members)
        #     print(f"hobby : {hobby.name} / hobby members : {hobby_members}")
        # # 역참조를 사용하지 않았을 때
        # # user_profile = UserProfile.objects.get(user=user)
        # # hobbys = user_profile.hobby.all()


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

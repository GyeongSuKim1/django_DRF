from rest_framework.permissions import BasePermission
from datetime import datetime, timedelta
from django.utils import timezone

from rest_framework.exceptions import APIException
from rest_framework import status

'''
datetime field와 비고 시
(tatetime)user.join_date > datetime.now **에러**
(tatetime)user.join_date > timezone.now **정상**

Date field : 2020-xx-xx
DateTime field : 2020-xx-xx 10:30:00
'''


class RegistedMoreThanAWeekUser(BasePermission):    # 가입후 7일 지나야 게시글 작성 가능
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:   # 인증된 사용자만 접근 시키기
            return False

        # if user.join_date < (datetime.now().date() - timedelta(days=7)):
        #     return True
        print(f"user join date : {user.join_date}")
        print(f"now date : {datetime.now().date()}")
        print(f"a weej agi date : {datetime.now().date() - timedelta(days=7)}")
        return bool(user.join_date < (timezone.now() - timedelta(minutes=1)))


class RegistedMoreThanDaysUser(BasePermission):
    message = '게시글은 가입 일로부터 3일 뒤에 작성할 수 있습니다.'

    def has_permission(self, request, view):
        user = request.user

        # return bool(user.is_authenticated and
        #             request.user.join_date < (timezone.now() - timedelta(minutes=3))) # 한줄로 쓰기

        if not user or not user.is_authenticated:
            return False

        return bool(user.join_date < (timezone.now() - timedelta(minutes=3)))


# ㅡㅡ 로그인을 하지 않은 사용자 ㅡㅡ
class GenericAPIException(APIException):
    def __init__(self, status_code, detail=None, code=None):
        self.status_code = status_code
        super().__init__(detail=detail, code=code)

# ㅡㅡ 로그인을 한 사용자 ㅡㅡ


class IsAdminOrIsAuthenticatedReadOnly(BasePermission):
    """
    admin 사용자는 모두 가능, 로그인 사용자는 조회만 가능(게시글은 7일 뒤부터)
    """
    SAFE_METHODS = ('GET', )    # 메소드를 지정 해줄수 있음
    message = '게시글은 가입 일로부터 7일 뒤에 작성할 수 있습니다.'

    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            response = {
                "detail": "서비스를 이용하기 위해 로그인 해주세요.",
            }
            raise GenericAPIException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail=response)

        # user 가 인증된 사용자 이면서 리퀘스트 메소드가 세이프 메소드 안에 있을 때
            # 즉, 로그인 사용자가 get요청 시 True
        if user.is_authenticated and request.method in self.SAFE_METHODS:
            return True

        # admin 사용자 이거나 가입일이 7일 이상 된 사용자의 경우 True
        if user.is_authenticated and user.is_admin or user.join_date < (timezone.now() - timedelta(minutes=5)):
            return True

        return False

    '''
    따로 선언 하는 이유는 로그인이 되지 않은 사용자는 내부적으로 타는 로직이 다름
    즉, 로그인을 한 사용자가 POST를 하다가 접근 권한이 없는거랑 
    로그인하지 않은 사용자가 접근 권한이 없는거랑 다름
    그래서 로그인 한 사용자 + 로그인하지 않은 사용자 두개를 지정 해줘야 함
    '''

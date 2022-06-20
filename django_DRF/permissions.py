from rest_framework.permissions import BasePermission
from datetime import datetime, timedelta
from django.utils import timezone


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

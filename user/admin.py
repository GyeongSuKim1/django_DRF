from django.contrib import admin
from user.models import User as UserModel
from user.models import UserProfile as UserProfileModel
from user.models import Hobby as HobbyModel

# 커스텀 admin import
from django.contrib.auth.admin import UserAdmin as BaceUserAdmin


'''
 사용 방법은 TabulaInline과 StackedInline 모두 동일
 둘 다 사용해보고 뭐가 좋은지 비교해보기
 역참조 모델에서만 사용 가능
 class UserProfileInline(admin.TabulaInline):
 '''
class UserProfileInline(admin.StackedInline):
    model = UserProfileModel
    filter_horizontal = ['hobby']


'''
    커스텀 admin
    UserAdmin 테이블을 만들어 
    UserModel에 상속 시켜줌
'''
class UserAdmin(BaceUserAdmin):
    list_display = ('id', 'username', 'fullname',
                    'email')  # obj 목록에 띄워줄 필드를 지정
    # obj 목록에서 클릭 시 상세 페이지로 들어갈 수 있는 필드를 지정
    list_display_links = ('username', )
    list_filter = ('username', )    # filter를 걸 수 있는 필드를 생성 Ex) 그룹을 만듬
    search_fields = ('username', 'fullname', 'email', )  # 검색에 사용될 필드를 지정

    # 상세페이지에서 필드를 분류하는데 사용
    fieldsets = (
        ("info", {'fields': ('username', 'password',
         'email', 'fullname', 'join_date',)}),
        ('permissions', {'fields': ('is_admin', 'is_active')}),
    )
    filter_horizontal = []

    # 이렇게 하지 않고 따로 readonly_fields로 값을 주면 user를 만들때도 readonly상태가 됨
    def get_readonly_fields(self, request, obj=None):
        if obj:
            # obj가 특정 되었을 때 username도 eadonly에 포함
            return ('username', 'join_date', )
        else:
            return ('join_date', )  # 아니라면 join_date만 포함

    inlines = (UserProfileInline,)


admin.site.register(UserModel, UserAdmin)
admin.site.register(UserProfileModel)
admin.site.register(HobbyModel)

# 시리얼라이즈를 임포트 해줌
from pyexpat import model
from statistics import mode
from rest_framework import serializers

# user models 에서 모델을 가져 옴
from user.models import User as UserModel, UserProfile
from user.models import UserProfile as UserProfileModel
from user.models import Hobby as HobbyModel


class HobbySerializer(serializers.ModelSerializer):
    same_hobby_users = serializers.SerializerMethodField()  # 같은 취미를 가지고 있는 사람 찾기
    def get_same_hobby_users(self, obj):
        # obj : hobby model의 object
        # user_list = []    # 리스트 축약식 쓰기 전
        # for user_profile in obj.userprofile_set.all():
        #     user_list.append(user_profile.user.username)

        return [up.user.username for up in obj.userprofile_set.all()]   # 리스트 축약식
    
    class Meta:
        model = HobbyModel
        fields = ["name", "same_hobby_users"]


class UserProfileSerializer(serializers.ModelSerializer):
    # ManyToMany관계기 떄문에 쿼리셋으로 들어감
    hobby = HobbySerializer(many=True)  # input data 가 quertset일 경우 many=True
    
    class Meta:
        model = UserProfileModel
        fields = ["introduction", "birthday", "age", "hobby"]


class UserSerializer(serializers.ModelSerializer):  # ModelSerializer를 상속을 받음
    user_detail = UserProfileSerializer(source="userprofile")   # OneToOne 이라 object로 들어감

    class Meta: 
        '''
        메타 클래스가 시리얼라이즈 에서 제일 중요 함
            user serializers 에선 모델, 필드 두 가지가 가장 중요 함
        '''
        model = UserModel   # UserModel을 사용하여 serializer를 만들 것 이기 때문에 UserModel을 넣어 줌
        fields = ["username", "email", "fullname", "join_date", "user_detail"]

'''
UserSerializer 에서 model과 fields 를 지정을 해줘서 model안에 있는 데이터 중 
fields 로 적은 데이터들을 json 형식으로 return 해줌 
'''

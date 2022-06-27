# 시리얼라이즈를 임포트 해줌
from pyexpat import model
from re import A
from statistics import mode
from urllib import request
from rest_framework import serializers

# user models 에서 모델을 가져 옴
from user.models import User as UserModel, UserProfile
from user.models import UserProfile as UserProfileModel
from user.models import Hobby as HobbyModel
from blog.models import Article as ArticleModel
from blog.models import Comment as CommentModel



# 전역 변수
VALID_EMAIL_LIST = ["naver.com", "gamil.com", "yahoo.com"]





class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = "__all__"
        
    def create(self, *args, **kwargs):
        user = super().create(*args, **kwargs)
        password = user.password
        user.set_password(password)
        user.save()
        return user
    
    def update(self, *args, **kwargs):
        user = super().update(*args, **kwargs)
        password = user.password
        user.set_password(password)
        user.save()
        return user
        
        
# ㅡㅡ Comment return ㅡㅡ
class CommentsSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    
    def get_user(self, obj):
        return obj.user.username
        
        
    class Meta:
        model = CommentModel
        fields = ["user", "contents"]
        
        
# ㅡㅡ Article return ㅡㅡ
class ArticlesSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    comments = CommentsSerializer(many=True, source="comment_set", read_only=True)
    
    def get_category(self, obj):
        return[category.name for category in obj.category.all()]
        
    class Meta:
        model = ArticleModel
        fields = ["user", "category", "title", "content", "comments", 
                  "exposure_start", "exposure_end", ]
        


# ㅡㅡ 같은 취미 값 return ㅡㅡ
class HobbySerializer(serializers.ModelSerializer):
    same_hobby_users = serializers.SerializerMethodField()  # 같은 취미를 가지고 있는 사람 찾기
    def get_same_hobby_users(self, obj):
        # obj : hobby model의 object
        # user_list = []    # 리스트 축약식 쓰기 전
        # for user_profile in obj.userprofile_set.all():
        #     user_list.append(user_profile.user.fullname)
        user = self.context["request"].user # 나의 이름 제외

        return [up.user.fullname for up in obj.userprofile_set.exclude(user=user)]   # 리스트 축약식
    
    class Meta:
        model = HobbyModel
        fields = ["name", "same_hobby_users"]


# ㅡㅡ 유저 정보 return ㅡㅡ
class UserProfileSerializer(serializers.ModelSerializer):
    # ManyToMany관계기 떄문에 쿼리셋으로 들어감
    hobby = HobbySerializer(many=True, read_only=True)  # input data 가 quertset일 경우 many=True
    get_hobbys = serializers.ListField(required=False)
    
    class Meta:
        model = UserProfileModel
        fields = ["introduction", "birthday", "age", "hobby", "get_hobbys"]


# ㅡㅡ 유저 게시글 return ㅡㅡ
class UserSerializer(serializers.ModelSerializer):  # ModelSerializer를 상속을 받음
    user_detail = UserProfileSerializer(source="userprofile")   # OneToOne 이라 object로 들어감
    articles = ArticlesSerializer(many=True, source="article_set", read_only=True)
    comments = CommentsSerializer(many=True, source="comment_set", read_only=True)
    
    # login_user_fullname = serializers.SerializerMethodField()
    # def get_login_user_fullname(self, obj):
    #     return self.context["request"].user.fullname
    # def validate(self, data):
    #     # if data  :
    #     # return data
    
    # Validate : 기존 validate + custom validation
    def validate(self, data):
        if data.get("email", "").split("@")[-1] not in VALID_EMAIL_LIST:
            raise serializers.ValidationError(
                detail={"error": "유효 한 이메일 주소가 아닙니다."}
            )

        if not data.get("fullname", "").startswith("김"):
            raise serializers.ValidationError(
                detail={"error": "김씨만 가입 가능"}
            )

        return data
    
    # 기존 함수를 덮어씀
    def create(self, validated_data):
        user_profile = validated_data.pop("userprofile")
        get_hobby = user_profile.pop("get_hobbys", [])
        password = validated_data.pop("password")
        
        user = UserModel(**validated_data)
        user.set_password(password)
        user.save()
        
        
        user_profile = UserProfileModel.objects.create(user=user, **user_profile)
        
        user_profile.hobby.add(*get_hobby)
        
        return user
    
    
    def update(self, instance, validated_data):
            # instance에는 입력된 object가 담긴다.
            # print(f"147 번 줄 : {instance}")
            # print(f"148 번 줄 : {validated_data }")
        user_profile = validated_data.pop("userprofile")
        get_hobbys = user_profile.pop("get_hobbys", [])
        
        for key, value in validated_data.items():   # 딕셔너리의 키 벨류를 선언 해줌
            if key == "password":
                instance.set_password(value)
                continue
            setattr(instance, key, value)   # setattr 따로 검색해서 알아보자
        instance.save()
        
        user_profile_object = instance.userprofile
        for key, value in user_profile.items():
            setattr(user_profile_object, key, value)   # 역참조
            
        user_profile_object.save()
        user_profile_object.hobby.set(get_hobbys)
        return instance
    
    
    class Meta: 
        model = UserModel   # UserModel을 사용하여 serializer를 만들 것 이기 때문에 UserModel을 넣어 줌
        fields = ["username", "password", "email", "fullname", "join_date", 
                  "user_detail", "articles", "comments",]

        # 각 필드에 해당하는 다양한 옵션 지정
        extra_kwargs = {
            # write_only : 해당 필드를 쓰기 전용으로 만들어 준다.
            # 쓰기 전용으로 설정 된 필드는 직렬화 된 데이터에서 보여지지 않는다.
            'password': {'write_only': True}, # default : False
            'email': {
                # error_messages : 에러 메세지를 자유롭게 설정 할 수 있다.
                'error_messages': {
                    # required : 값이 입력되지 않았을 때 보여지는 메세지
                    'required': '이메일을 입력해주세요.',
                    # invalid : 값의 포맷이 맞지 않을 때 보여지는 메세지
                    'invalid': '알맞은 형식의 이메일을 입력해주세요.'
                    },
                    # required : validator에서 해당 값의 필요 여부를 판단한다.
                    'required': False # default : True
                    },
            }


'''
메타 클래스가 시리얼라이즈 에서 제일 중요 함
    user serializers 에선 모델, 필드 두 가지가 가장 중요 함

UserSerializer 에서 model과 fields 를 지정을 해줘서 model안에 있는 데이터 중 
fields 로 적은 데이터들을 json 형식으로 return 해줌 
'''

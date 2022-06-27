from datetime import datetime
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import status
from user.serializers import UserSerializer
from .models import Article as ArticleModel
from django_DRF.permissions import RegistedMoreThanDaysUser
from user.models import User as UserModle

from user.serializers import ArticlesSerializer

from django_DRF.permissions import IsAdminOrIsAuthenticatedReadOnly
class ArticleView(APIView):
    # permission_classes = [permissions.IsAuthenticated] # 로그인 된 사용자만 view 조회 가능
    # permission_classes = [RegistedMoreThanDaysUser] # 커스텀 된 permissions
    
    # admin 사용자는 모두 가능, 로그인 사용자는 조회만 가능 (게시글은 7일 뒤 부터)
    permission_classes = [IsAdminOrIsAuthenticatedReadOnly]
    
    def get(self, request):
        time = datetime.now()
        articles = ArticleModel.objects.filter(
            exposure_start__lte=time,
            exposure_end__gte=time,
        ).order_by("-id")
        return Response(ArticlesSerializer(articles, many=True).data, status=status.HTTP_200_OK)
        
        # order_bj 연습 코드
        # article = ArticleModel.objects.all().order_by("-id")
        # print('18번 줄 : ',article)
        # return Response({ })
        
        # user = request.user
        # articles = ArticleModel.objects.filter(user=user)
        # titles = [article.title for article in articles]    # list 축약 문법
        # contents = [article.content for article in articles]

        # titles = []
        # for article in articles:
        #     titles.append(article.title)

        # return Response({"title": titles, "content": contents})

    def post(self, request):
        user = request.user
        request.data['user'] = user.id
        article_serializer = ArticlesSerializer(data=request.data)
        
        # is_valid : 아티클 시리얼라이져의 유효성을 검증 해줌 (True or False로 결과 값 나옴)
        if article_serializer.is_valid():
            article_serializer.save()
            return Response(article_serializer.data, status=status.HTTP_200_OK)
        
        return Response(article_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
        ''' 시리얼라이져로 이동
        user = request.user
        title = request.data.get("title", "")
        content = request.data.get("content", "")
        categorys = request.data.get("category", [])    # 카테고리는 리스트 형태로 보내줌
        exposure_start = request.data.get("exposure_start")
        exposure_end = request.data.get("exposure_end")
        
        
        if len(title) <= 5:
            return Response({"error": "title은 5자 이상 작성 해주세요."}, status=status.HTTP_400_BAD_REQUEST)
        
        if len(content) <= 20:
            return Response({"error": "content는 20자 이상 작성 해주세요."}, status=status.HTTP_400_BAD_REQUEST)
        
        if not categorys:
            return Response({"error": "category를 작성하지 않았습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        article = ArticleModel(
            user=user,
            title=title,
            content = content,
            exposure_start = exposure_start,
            exposure_end = exposure_end,
        )
        article.save()  # 저장 해주고
        article.category.add(*categorys)    # category.add를 해주어 *category를 통해 리스트를 풀어 줌
        return Response({"message": "게시글작성 성공 ! "}, status=status.HTTP_200_OK)
        '''
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import status
from .models import Article as ArticleModel
from user.serializers import UserSerializer
from django_DRF.permissions import RegistedMoreThanDaysUser
from user.models import User as UserModle


class ArticleView(APIView):
    # permission_classes = [permissions.IsAuthenticated] # 로그인 된 사용자만 view 조회 가능
    permission_classes = [RegistedMoreThanDaysUser] # 커스텀 된 permissions

    def get(self, request):
        article = ArticleModel.objects.all().order_by("-id")
        print('18번 줄 : ',article)
        return Response({ })
        
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
        title = request.data.get("title", "")
        content = request.data.get("content", "")
        categorys = request.data.get("category", [])    # 카테고리는 리스트 형태로 보내줌

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
        )
        article.save()  # 저장 해주고
        article.category.add(*categorys)    # category.add를 해주어 *category를 통해 리스트를 풀어 줌
        return Response({"message": "게시글작성 성공 ! "}, status=status.HTTP_200_OK)
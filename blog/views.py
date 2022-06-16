from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from .models import Article as ArticleModel


class ArticleView(APIView):
    permission_classes = [permissions.IsAuthenticated] # 로그인 된 사용자만 view 조회 가능

    def get(self, request):
        user = request.user
        articles = ArticleModel.objects.filter(user=user)

        titles = [article.title for article in articles]    # list 축약 문법
        titles = []

        for article in articles:
            titles.append(article.title)

        return Response({"title": titles})

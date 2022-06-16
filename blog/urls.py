
from django.contrib import admin
from django.urls import path, include
from blog import views

urlpatterns = [
    path('article/', views.ArticleView.as_view()),  # CBV 는 위에 as_view()를 적어줘야 함
]

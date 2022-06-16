
from django.contrib import admin
from django.urls import path, include
from user import views

urlpatterns = [
    # user/
    path('', views.UserView.as_view()),  # CBV 는 위에 as_view()를 적어줘야 함
    path('login/', views.UserAPIView.as_view()),
    path('logout/', views.UserAPIView.as_view()),
]

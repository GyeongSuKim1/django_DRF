from django.urls import path, include
from product import views

'''
순서가 중요함 django 에서 url을 보고 매칭을 위에서 부터 해준다.
고로 변수명 url보단 아무것도 없는 것이 위로 와야 한다.
'''

urlpatterns = [
    path('', views.ProductView.as_view()),
    path('<product_id>/', views.ProductView.as_view()),
]
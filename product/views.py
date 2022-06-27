from datetime import datetime
from functools import partial
from django.shortcuts import render
# APIView 를 import 해주자
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.db.models.query_utils import Q
from product.models import product as ProductModel
from product.serializers import ProductSerializer



class ProductView(APIView):
    def get(self, request):
        '''
        프론트를 가져오는 것 이기 때문에 get으로 product
        현재시간을 먼저 알아야 함 datetime을 임포트 해주고
        datetime.now() 작성
        프로덕트 모델을 가져옴
        filter 에 조건을 걸어주자
        첫번째 조건 : 시작 일자가 오늘보다 전이여야 하고 끝난 일자가 오늘 이후여야 함 
        유저가 로그인한 유저 즉, 나 이면 다 가져와라
        '''
        today = datetime.now()

        # product를 db에서 불러옴
        products = ProductModel.objects.filter(
            Q(exposure_start_date__lte=today, exposure_end_date__gte=today,) | 
            Q(user=request.user)
        )

        # 불러온 product를 ProductSerializer에 넣어주고 list형식이기 때문에 manye=True
        serialized_data = ProductSerializer(products, many=True).data

        return Response(serialized_data, status=status.HTTP_200_OK)


    def post(self, request):
        '''
        * 한번에 정보 받아오는 법*
        기존에 쓰던 방식인 user = request.user를 사용하지 않고 진행
        request.user.id 정보를 request.data 안에 user라는 키 값안에 저장 해줌
        '''
        request.data['user'] = request.user.id
        product_serializers = ProductSerializer(data=request.data)
        
        # 검증 시작
        if product_serializers.is_valid():
            product_serializers.save()  # 검증이 통과가 된다면 save 저장 해줌
            return Response(product_serializers.data, status=status.HTTP_200_OK)    # 검증 통과
        else:
            return Response(product_serializers.errors, status=status.HTTP_400_BAD_REQUEST) # 검증 실패
        
        
    '''
    업데이트에서 가장 중요한건 어느 글 인지 찾는 것
    어느 글이냐는 DB를 보면 각각의 글마다 고유한 id값 (PK)이 있다.
    이 id로 특정을 해줘야 함
    주소 url에 리소스 라는 것이 매핑이 되어 있어야 함
    '''
    def put(self, request, product_id): # url에서 product_id를 받아오자
        product = ProductModel.objects.get(id=product_id)   # db에서 Modle을 가져와서 product_id안에 id 값을 담자
        # 우리가 불러왔던 product 데이터를 시리얼라이저에 넣어주고 
        #   그중 request받은 data를 새롭게 업데이트 시켜준다는 의미
        product_serializers = ProductSerializer(product, data=request.data, partial=True)   # partial : 일부만 바꿀수 있게 해줌

        if product_serializers.is_valid():
            product_serializers.save()  # 검증이 통과가 된다면 save 저장 해줌
            return Response(product_serializers.data, status=status.HTTP_200_OK)    # 검증 통과
        else:
            return Response(product_serializers.errors, status=status.HTTP_400_BAD_REQUEST) # 검증 실패
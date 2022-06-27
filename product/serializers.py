from rest_framework import serializers

from product.models import product as ProductModel


class ProductSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field='fullname')
    
    class Meta:
       model = ProductModel
       fields = "__all__"
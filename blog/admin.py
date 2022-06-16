from django.contrib import admin
from .models import Category as CategoryModel
from .models import Article as ArticleModel

# Register your models here.
admin.site.register(CategoryModel)
admin.site.register(ArticleModel)
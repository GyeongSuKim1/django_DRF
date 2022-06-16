from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField("이름", max_length=50)
    description = models.TextField("설명", max_length=255)
    
    def __str__(self):
        return self.name
    
class Article(models.Model):
    user = models.ForeignKey('user.User', verbose_name='작성자', on_delete=models.CASCADE)
    title = models.CharField("제목", max_length=100)
    category = models.ManyToManyField(Category, verbose_name=("카테고리"))
    content = models.TextField("내용", max_length=255)
    
    def __str__(self):
        return f'{self.user.username} 님이 작성하신 게시글.'
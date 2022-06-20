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
    category = models.ManyToManyField(Category, verbose_name=("category"))
    content = models.TextField("내용", max_length=255)
    
    def __str__(self):
        return f'{self.user.username} 님이 작성하신 게시글.'
    

class Comment(models.Model):
    user = models.ForeignKey('user.User', verbose_name='작성자', on_delete=models.CASCADE)
    article = models.ForeignKey('Article', verbose_name='게시글', on_delete=models.CASCADE)
    contents = models.TextField("본내용", max_length=500)
    
    def __str__(self):
        return f"{self.article.title} : {self.contents}"
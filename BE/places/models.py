from django.db import models

# Create your models here.
# Create your models here.
class Place(models.Model):   # 장고 기본 user와 호환되고, 우리 프로젝트에 맞는 새로운 유저 생성
    city = models.CharField(max_length=30)
    category = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    number = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    imgUrl = models.CharField(max_length=100)
    def __str__(self):
        return self.name
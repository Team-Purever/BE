from django.db import models
from django.contrib.auth.models import AbstractUser

class Provider(models.TextChoices):
    KAKAO = 'KAKAO', 'KAKAO'
    GOOGLE = 'GOOGLE', 'GOOGLE'
    NAVER = 'NAVER', 'NAVER'

# Create your models here.
class User(AbstractUser):   # 장고 기본 user와 호환되고, 우리 프로젝트에 맞는 새로운 유저 생성
    platFormId = models.CharField(max_length=200, unique=True)
    provider = models.CharField(max_length=30, choices=Provider.choices)
    nickname = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    number = models.CharField(max_length=100)
    def __str__(self):
        return self.name
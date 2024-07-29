from django.db import models
from auths.models import User

class Diary(models.Model):   
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='diaries')
    pet_id = models.PositiveIntegerField()
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=300)
    url = models.CharField(max_length=300)

    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.content

class Image(models.Model):   
    url = models.ImageField(null=True, upload_to="", blank=True) # 이미지 컬럼 추가
    def __str__(self):
        return self.url
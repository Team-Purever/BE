from django.db import models
from auths.models import User

# Create your models here.
class Pet(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pets', null=True)
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    photo = models.ImageField(upload_to='pet_photos/')

    def __str__(self):
        return self.name
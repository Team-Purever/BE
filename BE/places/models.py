from django.db import models

class Place(models.Model):
    city = models.CharField(max_length=30)
    category = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    number = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    imgUrl = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
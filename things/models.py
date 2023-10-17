from django.db import models
# Create your models here.

class Thing(models.Model):
  name = models.TextField(max_length=50)
  description = models.TextField()
  quantity = models.IntegerField()
  

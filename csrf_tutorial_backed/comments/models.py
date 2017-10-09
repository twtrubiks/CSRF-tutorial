from django.db import models


# Create your models here.
class Comment(models.Model):
    name = models.TextField(max_length=20)
    text = models.TextField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

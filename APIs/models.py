from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Blog(models.Model):
    user_assoc = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=32)
    content = models.TextField(null=True, blank=True, default=None)
    image = models.ForeignKey('Image', on_delete=models.SET_NULL, null=True)
    is_deleted = models.BooleanField()
    def __str__(self) :
        return self.title

class Image(models.Model):
    image = models.ImageField(upload_to='images/')
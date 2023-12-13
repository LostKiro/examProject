from django.contrib.auth.models import User
from django.db import models

class ModelPavel(models.Model):
    name = models.CharField(max_length=10)
    email = models.CharField(max_length=20)
    surname = models.CharField(max_length=10)
    password = models.CharField(max_length=10)


class ModelPavelImg(models.Model):
    name = models.CharField(max_length=10)
    img = models.ImageField(upload_to='imgs')

class UserProfile(models.Model):
    login = models.CharField(max_length = 20)
    password = models.CharField(max_length=20)
    email = models.CharField(max_length=20)
    avatar = models.ImageField(upload_to='avatars/')


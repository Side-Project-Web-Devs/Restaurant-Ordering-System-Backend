from email.policy import default
from django.db import models
from django.contrib.auth.models import User


class Userprofile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="profiles/user.png")

    def __str__(self):
        return str(self.user)


class Customer(models.Model):

    name = models.CharField(max_length=150)
    table_number = models.IntegerField()
    slug = models.SlugField(max_length=150)

    def __str__(self):
        return self.name

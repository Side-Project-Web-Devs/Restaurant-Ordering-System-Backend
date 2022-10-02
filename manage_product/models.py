from email.policy import default
from pyexpat import model
from tkinter import CASCADE
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User
from django.forms import BooleanField
from main.models import Customer
from django.core.validators import MaxLengthValidator


class Manage_product(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user")
    product_name = models.CharField(max_length=200, default="", blank=False)
    description = models.TextField(max_length=1000, default="", blank=False)
    image = models.ImageField(upload_to='product_image', blank=False)
    price = models.IntegerField(blank=False)
    availability = models.BooleanField(default=True)
    slug = models.SlugField(max_length=250, null=True)

    def __str__(self):
        return self.product_name


class Add_to_cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(
        Manage_product, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(blank=False)
    status = models.CharField(
        max_length=100, null=True, blank=True, default="")
    to_di = models.CharField(max_length=10, blank=False)
    if_seen = models.IntegerField(null=True)
    slug = models.SlugField(max_length=500, null=True)

    def __str__(self):
        return str(self.customer) + " order " + str(self.order)


class Feedback(models.Model):
    cus = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    ord = models.ForeignKey(Add_to_cart, on_delete=models.SET_NULL, null=True)
    feedback = models.TextField(blank=True, default="")
    reply = models.TextField(blank=True, default="")

    def __str__(self):
        return str(self.cus) + " order " + str(self.ord)

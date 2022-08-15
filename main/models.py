from django.db import models

class Customer(models.Model):

    name = models.CharField(max_length=150, null=True)
    table_number = models.IntegerField()
    slug = models.SlugField(max_length=150, null=True)

    def __str__(self):
        return self.name
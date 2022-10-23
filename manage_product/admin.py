from MySQLdb import Date
from django.contrib import admin
from .models import Inventory, Manage_product, Add_to_cart, Feedback, Date_inv

admin.site.register(Manage_product)
admin.site.register(Add_to_cart)
admin.site.register(Feedback)
admin.site.register(Inventory)
admin.site.register(Date_inv)

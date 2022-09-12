from django.urls import path, include
from . import views


urlpatterns = [
    path('qrcode_generator/', views.qrcode, name='qrcode_generator'),
    path('delete_qr/<int:id>/', views.delete_qr, name="delete_qr"),
]

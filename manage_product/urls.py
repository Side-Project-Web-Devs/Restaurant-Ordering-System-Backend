from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
   path('add_product/', views.add_product, name='add_product'),
   path('edit_product/<slug:slug>/', views.edit_product, name='edit_product'),
   path('delete_product/<slug:slug>/', views.delete_product, name='delete_product'),
   path('add_to_cart/<slug:customer>/<slug:order>/', views.customer_addcart, name='add_to_cart'),
   path('cart/<slug:customer>/', views.customer_cart, name='customer_cart'),
   path('place_order/<slug:slug>/', views.place_order, name='place_order'),
   path('customer_order', views.view_customer_order, name='customer_order'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
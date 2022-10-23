from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('add_product/', views.add_product, name='add_product'),
    path('edit_product/<slug:slug>/', views.edit_product, name='edit_product'),
    path('delete_product/<slug:slug>/',
         views.delete_product, name='delete_product'),
    path('availability/<slug:slug>',
         views.product_availability, name='unavailable'),
    path('return_availability/<slug:slug>/',
         views.return_availability, name='available'),
    path('feedback_admview/', views.feedback_admview, name="feedback_admview"),
    path('feedback_reply/<int:id>/', views.feedback_reply, name="feedback_reply"),
    path('delete_reply/<int:id>/', views.delete_reply, name="delete_reply"),
    path('inventory/', views.inventory, name="inventory"),
    path('edit_inventory/<int:id>/', views.edit_inventory, name='edit_inventory'),

    path('add_to_cart/<slug:customer>/<slug:order>/',
         views.customer_addcart, name='add_to_cart'),
    path('cart/<slug:customer>/', views.customer_cart, name='customer_cart'),
    path('edit_cart/<int:id>/', views.edit_cart, name='edit_cart'),
    # path('checkbox/<int:id>/', views.checkbox, name='checkbox'),
    path('my_order/<slug:slug>/', views.my_order, name='my_order'),
    path('received/<int:id>/', views.receive_order, name='received'),
    path('feedback/<int:id>/', views.feedback, name='feedback'),
    path('feedback_cusview/<slug:slug>/',
         views.feedback_cusview, name='feedback_cusview'),

    path('customer_list/', views.customer_list, name='customer_list'),
    path('total_order/', views.total_order, name='total_order'),
    path('customer_order/<slug:slug>/',
         views.view_customer_order, name='customer_order'),
    path('confirm_order/<int:id>/', views.confirm_order, name='confirm_order'),
    path('serve_order/<int:id>/', views.serve_order, name='serve_order'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)

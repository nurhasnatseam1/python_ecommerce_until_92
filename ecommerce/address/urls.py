from django.urls import path
from .views import checkout_address_create_view,checkout_address_reuse_view
app_name='address'


urlpatterns=[
    path('checkout_address_create/',checkout_address_create_view,name='checkout_address_create'),
    path('checkout_address_reuse/',checkout_address_reuse_view,name='checkout_address_reuse')
]

from django.urls import path
from .views import cart_home,cart_update,checkout_home
app_name="carts"



urlpatterns=[
    path('',cart_home,name="cart_home"),
    path('update/',cart_update,name='cart_update'),
    path('checkout/',checkout_home,name='checkout_home'),
]

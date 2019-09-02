from django.urls import path
from .views import loginView,registerView,guestLoginView
from django.contrib.auth.views import LogoutView
app_name='accounts'
urlpatterns=[
    path('login/',loginView,name='login'),
    path('register/',registerView,name='register'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('guest_login/',guestLoginView,name='guest_login'),
]

from django.urls import path
from .views import ProductListView,ProductDetailSlugView

app_name='products'


urlpatterns=[
    path('',ProductListView.as_view(),name='products_list'),
    path('product/<slug>/',ProductDetailSlugView.as_view(),name='product_detail')
]


from django.urls import path
from catalog.views import home, contacts, last_5_products, product

app_name = 'catalog'

urlpatterns = [
    path('', home, name='home'),
    path('contacts/', contacts, name='contact'),
    path('last-5-products/', last_5_products, name='last_5_products'),
    path('product/', product, name='product'),
]
from django.urls import path
from django.views.decorators.cache import cache_page

from .views import (
    home,
    contacts,
    last_5_products,
    ProductCreateView,
    ProductListView,
    ProductDetailView,
    ProductUpdateView,
    ProductDeleteView,
    EntryCreateView,
    EntryListView,
    EntryDetailView,
    EntryUpdateView,
    EntryDeleteView, CreateVersionView,CategoryListView,
)

app_name = 'catalog'

urlpatterns = [
    path('', home, name='home'),
    path('contacts/', contacts, name='contact'),
    path('last-5-products/', last_5_products, name='last_5_products'),

    path('products/', ProductListView.as_view(), name='products'),
    path('product/<int:pk>/', cache_page(60)(ProductDetailView.as_view()), name='product'),
    path('add_product/', ProductCreateView.as_view(), name='add_product'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='update_product'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='delete_product'),
    path('products/<int:product_id>/create_version/', CreateVersionView.as_view(), name='create_version'),


    path('categories/', CategoryListView.as_view(), name='categories'),

    path('blog/', EntryListView.as_view(), name='list_entry'),
    path('blog/<int:pk>/', EntryDetailView.as_view(), name='entry_details'),
    path('blog/add/', EntryCreateView.as_view(), name='add_entry'),
    path('blog/<int:pk>/update/', EntryUpdateView.as_view(), name='update_entry'),
    path('blog/<int:pk>/delete/', EntryDeleteView.as_view(), name='delete_entry'),
]

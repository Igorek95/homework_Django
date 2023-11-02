from django.urls import path
from catalog.views import home, contacts, last_5_products, ProductCreateView, ProductListView, ProductDetailView, \
    EntryCreateView, EntryListView, EntryDetailView, EntryDeleteView, EntryUpdateView

app_name = 'catalog'

urlpatterns = [
    path('', home, name='home'),
    path('contacts/', contacts, name='contact'),
    path('last-5-products/', last_5_products, name='last_5_products'),
    path('products/', ProductListView.as_view(), name='products'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product'),
    path('add_product/', ProductCreateView.as_view(), name='add_product'),
    path('blog/add_entry', EntryCreateView.as_view(), name='add_entry'),
    path('blog/', EntryListView.as_view(), name='list_entry'),
    path('blog/<int:pk>', EntryDetailView.as_view(), name='entry_details'),
    path('blog/<int:pk>/delete', EntryDeleteView.as_view(), name='delete_entry'),
    path('blog/<int:pk>/update', EntryUpdateView.as_view(), name='update_entry'),
]

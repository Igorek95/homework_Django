from django.http import HttpResponse
import logging
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from pytils.translit import slugify

from .forms import ProductForm, EntryForm
from .models import Product, BlogEntry


def last_5_products(request):
    latest_products = Product.objects.order_by('-created_at')[:5]
    return render(request, 'catalog/last_5_products.html', {'latest_products': latest_products})


def home(request):
    catalog = Product.objects.all()
    context = {'object_list': catalog}
    return render(request, 'catalog/home.html', context)


def contacts(request):
    if request.method == 'POST':
        data_name = request.POST.get('name')
        data_email = request.POST.get('email')
        data_phone = request.POST.get('phone')
        data_text = request.POST.get('message')
        with open('data.txt', 'w', encoding='utf-8') as file:
            file.write(data_name)
            file.write(data_email)
            file.write(data_phone)
            file.write(data_text)
        return HttpResponse('Данные отправлены успешно!')
    return render(request, 'contacts/contacts.html')


class ProductListView(ListView):
    model = Product
    paginate_by = 6
    context_object_name = 'products'
    template_name = 'catalog/products_list.html'

# def products(request):
#     products = Product.objects.all()
#     context = {'object_list': products}
#     return render(request, 'catalog/products_list.html', context)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_list.html'

# def product(requests, pk):
#     product = Product.objects.get(pk=pk)
#     context = {
#         'object': product
#     }
#     return render(requests, 'catalog/product_list.html', context)


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/add_product.html'


    def post(self, request, *args, **kwargs):
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            result = "<h5 style='background-color: #00b91f; color: black; border-radius: 7px; height: 30px; text-align: center;'>Продукт добавлен!</h5>"
            form = ProductForm()
        else:
            result = "<h5 style='background-color: #a50000; color: black; border-radius: 7px; height: 30px; text-align: center;'>Неправильно заполнены данные!</h5>"
        return render(request, self.template_name, {'form': form, 'result': result})

# def add_product(request):
#     result = ''
#     if request.method == 'POST':
#         form = ProductForm(request.POST, request.FILES)
#         if form.is_valid():
#             print(form.__dict__)
#             form.save()
#             result = "<h5 style='background-color: #00b91f; color: black; border-radius: 7px; height: 30px; text-align: center;'>Продукт добавлен!</h5>"
#             form = ProductForm()
#         else:
#             result = "<h5 style='background-color: #a50000; color: black; border-radius: 7px; height: 30px; text-align: center;'>Неправильно заполнены данные!</h5>"
#     else:
#         form = ProductForm()
#     return render(request, 'catalog/add_product.html', {'form': form, 'result': result})


class EntryCreateView(CreateView):
    model = BlogEntry
    form_class = EntryForm
    template_name = 'catalog/add_blog_entry.html'
    success_url = 'catalog:list_entry'

    def post(self, request, *args, **kwargs):
        form = EntryForm(request.POST, request.FILES)
        print(form.__dict__)
        if form.is_valid():
            saved_form = form.save()
            saved_form.entry_slug = slugify(
                saved_form.entry_title)
            saved_form.save()
            result = "<h5 style='background-color: #00b91f; color: black; border-radius: 7px; height: 30px; text-align: center;'>Запись добавлена!</h5>"
            form = EntryForm()
        else:
            result = "<h5 style='background-color: #a50000; color: black; border-radius: 7px; height: 30px; text-align: center;'>Неправильно заполнены данные!</h5>"
        return render(request, self.template_name, {'form': form, 'result': result})


class EntryDetailView(DetailView):
    model = BlogEntry
    template_name = 'catalog/blogentry_detail.html'
    context_object_name = 'entry'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class EntryListView(ListView):
    model = BlogEntry
    paginate_by = 6
    template_name = 'catalog/blogentry_list.html'

    def get_queryset(self):
        data = BlogEntry.objects.filter(
            is_published=True).order_by('-date_created')
        return data


class EntryUpdateView(UpdateView):
    model = BlogEntry
    form_class = EntryForm
    template_name = 'catalog/update_blog_entry.html'

    def form_valid(self, form):
        if form.is_valid():
            saved_form = form.save()
            saved_form.entry_slug = slugify(
                saved_form.entry_title)
            saved_form.save()
            EntryUpdateView.success_url = f'{reverse_lazy("catalog:list_entry")}{saved_form.pk}'
        return super().form_valid(form)


class EntryDeleteView(DeleteView):
    model = BlogEntry
    template_name = 'catalog/blogentry_confirm_delete.html'
    success_url = reverse_lazy('catalog:list_entry')
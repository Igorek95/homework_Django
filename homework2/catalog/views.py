from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from pytils.translit import slugify

from .forms import  EntryForm, VersionForm, ProductFormAdmin, ProductFormUser, ProductFormModerator
from .models import Product, BlogEntry, Version, Category
from .services  import get_category_list


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
    context_object_name = 'products'
    template_name = 'catalog/products_list.html'

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.has_perm('catalog.set_published'):
            data = Product.objects.all().order_by('-last_modified')
        else:
            data = Product.objects.filter(
                is_published=True).order_by('-last_modified')
        return data


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['version'] = Version.objects.get(
                product=context['object'], is_active=True)
        except:
            pass
        return context



class ProductCreateView(PermissionRequiredMixin, CreateView):
    model = Product
    template_name = 'catalog/product_form.html'
    permission_required = "catalog.add_product"
    success_url = reverse_lazy('catalog:products')

    def get_form_class(self):
        if self.request.user.is_superuser:
            self.form_class = ProductFormAdmin
        else:
            self.form_class = ProductFormUser
        return super().get_form_class()

    def form_valid(self, form):
        response = super().form_valid(form)
        result = "<h5 style='background-color: #00b91f; color: black; border-radius: 7px; height: 30px; text-align: center;'>Продукт добавлен!</h5>"
        return render(self.request, self.template_name, {'form': form, 'result': result})


class ProductUpdateView(UserPassesTestMixin,  UpdateView):
    model = Product
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:products')

    def get_form_class(self):
        if self.request.user.is_superuser:
            self.form_class = ProductFormAdmin
        elif self.request.user == self.object.user:
            self.form_class = ProductFormUser
        elif self.request.user.has_perm('catalog.set_published'):
            self.form_class = ProductFormModerator
        return super().get_form_class()

    def test_func(self):
        return self.request.user.is_superuser or \
            self.request.user == self.get_object().user or \
            self.request.user.has_perm('catalog.set_published')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['version_form'] = VersionForm()
        return context

    def create_version(request, pk):
        product = get_object_or_404(Product, pk=pk)

        if request.method == 'POST':
            version_form = VersionForm(request.POST)
            if version_form.is_valid():
                version_data = version_form.cleaned_data
                product.create_version(version_data)
                return redirect('catalog:product', pk=pk)
        else:
            version_form = VersionForm()

        return render(request, 'catalog/product_form.html', {'object': product, 'version_form': version_form})

class ProductDeleteView(PermissionRequiredMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    permission_required = "catalog.delete_product"
    success_url = reverse_lazy('catalog:products')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class EntryCreateView(PermissionRequiredMixin, CreateView):
    model = BlogEntry
    form_class = EntryForm
    template_name = 'catalog/add_blog_entry.html'
    success_url = 'catalog:list_entry'
    permission_required = "catalog.add_blogentry"

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


class EntryUpdateView(PermissionRequiredMixin, UpdateView):
    model = BlogEntry
    form_class = EntryForm
    permission_required = "catalog.change_blogentry"
    template_name = 'catalog/update_blog_entry.html'

    def form_valid(self, form):
        if form.is_valid():
            saved_form = form.save()
            saved_form.entry_slug = slugify(
                saved_form.entry_title)
            saved_form.save()
            EntryUpdateView.success_url = reverse_lazy('catalog:list_entry')
        return super().form_valid(form)


class EntryDeleteView(PermissionRequiredMixin, DeleteView):
    model = BlogEntry
    template_name = 'catalog/blogentry_confirm_delete.html'
    permission_required = "catalog.delete_blogentry"
    success_url = reverse_lazy('catalog:list_entry')


class CreateVersionView(CreateView):
    template_name = 'catalog/create_version.html'
    form_class = VersionForm
    model = Version
    context_object_name = 'versions'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_id = self.kwargs['product_id']
        context['object'] = get_object_or_404(Product, id=product_id)
        return context

    def form_valid(self, form):
        product_id = self.kwargs['product_id']
        product = get_object_or_404(Product, id=product_id)
        version = form.save(commit=False)
        version.product = product
        version.save()
        return redirect('catalog:product', pk=product_id)


class CategoryListView(ListView):
    model = Category
    context_object_name = 'categories'
    # template_name = 'catalog/product_list.html'

    def get_queryset(self):
        return get_category_list()
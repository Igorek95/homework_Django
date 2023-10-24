from django.http import HttpResponse
import logging
from django.shortcuts import render
from .models import Product


def last_5_products(request):
    latest_products = Product.objects.order_by('-created_at')[:5]
    return render(request, 'catalog/last_5_products.html', {'latest_products': latest_products})



def home(request):
    return render(request, 'catalog/home.html')


def contacts(request):
    if request.method == 'POST':
        data_name = request.POST.get('name')
        data_phone = request.POST.get('phone')
        data_text = request.POST.get('message')
        with open('data.txt', 'w', encoding='utf-8') as file:
            file.write(data_name)
            file.write(data_phone)
            file.write(data_text)
        return HttpResponse('Данные отправлены успешно!')
    return render(request, 'contacts/contacts.html')
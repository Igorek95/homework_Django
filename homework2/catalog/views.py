from django.http import HttpResponse
from django.shortcuts import render
import logging


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
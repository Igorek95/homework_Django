from catalog.models import Product, Category
from django import forms


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ("name", "description",
                  "image", "category", "price")
        categories = Category.objects.values('name', 'name')

        widgets = {
            "name": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название'
            }),
            "description": forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Описание'
            }),
            "image": forms.FileInput(attrs={
                'class': 'form-control',
                'placeholder': 'Картинка'
            }),
            "category": forms.Select(choices=categories, attrs={
                'class': 'form-control',
                'placeholder': 'Категория'
            }),
            "price": forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Цена в рублях'
            }),
        }
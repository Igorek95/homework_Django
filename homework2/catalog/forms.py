from django.urls import reverse

from .models import Product, Category, BlogEntry, Version
from django import forms


class ProductFormAdmin(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def create_version(self, version_data):
        version = self.versions.create(**version_data)
        return version

    def get_absolute_url(self):
        return reverse('catalog:product', args=[str(self.id)])

    def clean_name(self):
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']
        name = self.cleaned_data['name'].lower()
        for word in forbidden_words:
            if word in name:
                raise forms.ValidationError(f'Слово "{word}" запрещено в названии продукта.')
        return name

    def clean_description(self):
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']
        description = self.cleaned_data['description'].lower()
        for word in forbidden_words:
            if word in description:
                raise forms.ValidationError(f'Слово "{word}" запрещено в описании продукта.')
        return description


class ProductFormUser(ProductFormAdmin):

    class Meta:
        model = Product
        fields = ("name", "description",
                  "image", "category", "price")


class ProductFormModerator(ProductFormAdmin):

    class Meta:
        model = Product
        fields = ('description', 'is_published', 'category')


class VersionForm(forms.ModelForm):
    class Meta:
        model = Version
        fields = ['version_number', 'version_name', 'is_active']

    def __init__(self, *args, **kwargs):
        super(VersionForm, self).__init__(*args, **kwargs)


class EntryForm(forms.ModelForm):
    is_published = forms.BooleanField(required=False)

    class Meta:
        model = BlogEntry
        fields = ("entry_title", "entry_body", "entry_img", "is_published")

        widgets = {
            "entry_title": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Заголовок'
            }),
            "entry_body": forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Содержание записи'
            }),
            "entry_img": forms.FileInput(attrs={
                'class': 'form-control',
                'placeholder': 'Картинка'
            }),

        }
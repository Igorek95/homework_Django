from django.db import models

NULLABLE = {'null': True, 'blank': True}


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='product_images/', verbose_name='Изображение', **NULLABLE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за покупку')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    last_modified = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return f'{self.name} {self.price} {self.description} {self.category} '


class Contact(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    email = models.EmailField(verbose_name='Электронная почта')
    phone = models.CharField(max_length=15, verbose_name='Телефон')

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'

    def __str__(self):
        return self.name


class BlogEntry(models.Model):
    entry_title = models.CharField(
        max_length=150, verbose_name='заголовок')
    entry_slug = models.CharField(
        max_length=150, verbose_name='slug')
    entry_body = models.TextField(verbose_name='содержимое')
    entry_img = models.ImageField(
        upload_to='entry_img/', verbose_name='изображение', **NULLABLE)
    date_created = models.DateField(
        verbose_name="дата создания", auto_now_add=True)
    is_published = models.BooleanField(
        verbose_name="признак публикации", default=False)
    views_count = models.IntegerField(
        verbose_name="количество просмотров", default=0)

    def __str__(self):
        # Строковое отображение объекта
        return f'Название:{self.entry_title} Создание:{self.date_created} Опубликовано:{self.is_published} Просмотры:{self.views_count}'

    class Meta:
        verbose_name = 'Топик'  # Настройка для наименования одного объекта
        verbose_name_plural = 'Топики'  # Настройка для наименования набора объектов
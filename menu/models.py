from django.db import models
from django.urls import reverse

class MainCategories(models.Model):
    name = models.CharField('Название', max_length=250)
    picture = models.ImageField('Картинка', upload_to ='uploads/% Y/% m/% d/', null=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name = 'URL', null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category", kwargs={"category_slug": self.slug})
    
    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

class Products(models.Model):
    name = models.CharField('Наименование продукта', max_length=250)
    picture = models.ImageField('Картинка', upload_to = 'uploads/% Y/% m/% d/', null=True)
    title = models.TextField('Описание', blank=True)
    cat = models.ForeignKey(MainCategories, on_delete=models.PROTECT, null=True, verbose_name='Товары по катергорию')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name = 'URL', null=True)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("product", kwargs={"product_slug": self.slug})
    
    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ['id']
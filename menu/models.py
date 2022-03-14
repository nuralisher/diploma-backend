from django.db import models

class MainCategories(models.Model):
    name = models.CharField('Название', max_length=150)
    # picture = models.ImageField()
    # productsFromCategory = models.CharField('Продукты', max_length=150)
    
    def __str__(self):
        return self.name

class Products(models.Model):
    subName = models.ForeignKey(MainCategories, on_delete=models.CASCADE)
    

class Meta:
    verbose_name = 'Основная категория'
    verbose_name_plural = 'Основные категории'
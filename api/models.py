import uuid
from io import BytesIO
import qrcode
from django.contrib.auth.models import User
from django.core.files import File
from django.db import models
import qrcode.image.svg
from django.dispatch import receiver
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from user_management.models import Employee, Client


class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    employees = models.ManyToManyField(Employee, related_name='restaurants')
    owner = models.ForeignKey(Employee, related_name='my_restaurants', on_delete=models.CASCADE)


class Table(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True)
    number = models.IntegerField()
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='tables')

    class Meta:
        unique_together = ('restaurant', 'number')

    def __unicode__(self):
        return self.number


    def __int__(self):
        return self.number

    def save(self, *args, **kwargs):
        factory = qrcode.image.svg.SvgPathImage
        qrcode_img = qrcode.make(self.id, box_size=24, border=1,  image_factory=factory)
        buffer = BytesIO()
        qrcode_img.save(stream=buffer)
        fname = f'qr_code-{self.id}' + '.svg'
        self.qr_code.save(fname, File(buffer), save=False)
        super().save(*args, **kwargs)


@receiver(models.signals.post_delete, sender=Table)
def remove_file_from_s3(sender, instance, using, **kwargs):
    instance.qr_code.delete(save=False)


class MenuCategory(models.Model):
    name = models.CharField(max_length=255)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu_categories')


class Menu(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField()
    image = models.ImageField(upload_to='menu_images', blank=True)
    category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE, related_name='menus')

    def __str__(self):
        return self.name


@receiver(models.signals.post_delete, sender=Menu)
def remove_file_from_s3(sender, instance, using, **kwargs):
    instance.image.delete(save=False)


class PositionManager(models.Manager):
    def create_position(self, employee, restaurant, position):
        order_item = self.create(employee=employee, restaurant=restaurant, type=position)
        return order_item


class Position(models.Model):
    class PositionType(models.TextChoices):
        ADMIN = 'ADMIN', _('Админ')
        WAITER = 'WAITER', _('Официант')
    type = models.CharField(max_length=10, choices=PositionType.choices)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='positions')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='positions')

    class Meta:
        unique_together = ('employee', 'restaurant')

    objects = PositionManager()


class Call(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='calls')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='calls')
    # created = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now=True)
    table = models.OneToOneField(Table, on_delete=models.CASCADE, related_name='call')

    class CallType(models.TextChoices):
        CALL = 'CALL', _('Вызов')
        PAYMENT_WITH_CARD = 'PAYMENT_WITH_CARD', _('Оплата с картой')
        CASH_PAYMENT = 'CASH_PAYMENT', _('Оплата наличным')
    type = models.CharField(max_length=20, choices=CallType.choices)

    class CallStatus(models.TextChoices):
        OPEN = 'OPEN', _('Open')
        CANCELLED = 'CANCELLED', _('Cancelled')
        CLOSED = 'CLOSED', _('Closed')
    status = models.CharField(max_length=20, choices=CallStatus.choices,)


class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='orders')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='orders')
    comment = models.TextField(max_length=250, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='orders')


    # def get_total(self):
    #     total = 0
    #     for item in OrderItem.objects.filter(order=self):
    #         total = item.menu.price
    #     return total


class OrderItemManager(models.Manager):
    def create_order_item(self, menu, order, quantity):
        menu = Menu.objects.get(pk=menu)
        order_item = self.create(menu=menu, order=order, quantity=quantity)
        return order_item


class OrderItem(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='order_items')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.IntegerField()

    objects = OrderItemManager()


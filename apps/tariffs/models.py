from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from django.db.models.signals import post_save


User = get_user_model()


class Status(models.TextChoices):
     # Actual value ↓      # ↓ Displayed on Django Admin  
        ACTIVE   = 'Active', _('Active')
        INACTIVE = 'Inactive', _('Inactive')


class Tariff(models.Model):
    """"""
    name        = models.CharField('Название', max_length=255)
    energy_copy = models.PositiveIntegerField('energy copy', default=0)
    refil       = models.PositiveIntegerField(default=0)
    price_month = models.PositiveIntegerField(default=0)
    price_year  = models.PositiveIntegerField(default=0)
    economie    = models.PositiveIntegerField(default=0)
    storage     = models.FloatField(default=0)
    status      = models.CharField('Статус', max_length=10)
    products    = models.ManyToManyField("tariffs.Products", related_name="tariffs")
    stripeCustomerId     = models.CharField(max_length=255)
    stripeSubscriptionId = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name        = 'Тариф'
        verbose_name_plural = 'Тарифы'


class Products(models.Model):
    name        = models.CharField('Название', max_length=255)
    description = models.CharField('Описание', max_length=5000, blank=True)
    status      = models.CharField('Статус', choices=Status.choices, default='Active', max_length=10)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name        = 'Продукт'
        verbose_name_plural = 'Продукты'

    
class Payment(models.Model):
    user   = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment')
    status = models.BooleanField(default=False)
    date   = models.DateTimeField(auto_now_add=True)
    tariff = models.ForeignKey(Tariff, 
                               on_delete=models.SET_NULL,
                               null=True, blank=True, 
                               related_name='payment')
    amount = models.IntegerField(default=0)
    method = models.CharField(max_length=255, null=True, blank=True)
    session_id = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.user}|{self.status}|{self.date}|{self.amount}|{self.method}"

    class Meta:
        verbose_name        = 'Payment'
        verbose_name_plural = 'Payments'


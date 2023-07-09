from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


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
    status      = models.CharField('Статус', choices=Status.choices, default='Active', max_length=10)
    users       = models.ManyToManyField(User, related_name="tariff")
    products    = models.ManyToManyField("tariffs.Products", related_name="tariffs")

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

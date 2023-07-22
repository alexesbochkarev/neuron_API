from django.contrib import admin
from .models import Tariff, Products, Payment

class TariffAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
admin.site.register(Tariff, TariffAdmin)
admin.site.register(Products)
admin.site.register(Payment)

from django.contrib import admin
from .models import Tariff, Products, Payment

admin.site.register(Tariff)
admin.site.register(Products)
admin.site.register(Payment)

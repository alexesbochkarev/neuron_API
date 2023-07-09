from django.contrib import admin

# Register your models here.
from .models import Interests, Result, Tool

admin.site.register(Interests)
admin.site.register(Result)
admin.site.register(Tool)
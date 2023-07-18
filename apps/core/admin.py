from django.contrib import admin

# Register your models here.
from .models import Interests, Result, Tool, Privacy, WhiteList

class ResultAdmin(admin.ModelAdmin):
    list_display = ['id', 'created']

admin.site.register(Interests)
admin.site.register(Result, ResultAdmin)
admin.site.register(Tool)
admin.site.register(Privacy)
admin.site.register(WhiteList)
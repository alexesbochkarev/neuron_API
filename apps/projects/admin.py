from django.contrib import admin
from .models import Project, Post


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'name',]


class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created', 'modified', 'project', 'status']
    list_editable = ('status',)


admin.site.register(Project, ProjectAdmin)
admin.site.register(Post, PostAdmin)

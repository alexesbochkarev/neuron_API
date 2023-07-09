from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model


User = get_user_model()
                                  

class Project(models.Model):
    """"""
    name = models.CharField('Название', max_length=255)
    date = models.DateTimeField(_("date created"), default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    results = models.ManyToManyField('core.Result', related_name="projects")


    class Meta:
        verbose_name        = 'Проект'
        verbose_name_plural = 'Проекты'

    def __str__(self):
        return self.name
    

class Post(models.Model):
    """"""
    class Status(models.TextChoices):
     # Actual value ↓      # ↓ Displayed on Django Admin  
        DONE        = 'Done', _('Сделанно')
        SCHEDULED   = 'Scheduled', _('Запланировано')
        DRAFT       = 'Draft', _('Черновик')

    html        = models.CharField(max_length=100000, blank=True)
    title       = models.CharField(max_length=1000, blank=True)
    description = models.CharField(max_length=1000, blank=True)
    keywords    = models.CharField(max_length=1000, blank=True)
    date        = models.DateTimeField(null=True, blank=True)
    created     = models.DateTimeField(_("date created"), default=timezone.now)
    modified    = models.DateTimeField(_("date modified"), auto_now=True)
    status      = models.CharField('Статус', 
                                   choices=Status.choices, 
                                   default='Scheduled',
                                   max_length=10)
    project     = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='posts')

    class Meta:
        verbose_name        = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.status
    

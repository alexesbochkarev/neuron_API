from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


User = get_user_model()


class Interests(models.Model):
    """Интересы юзера"""
    name  = models.CharField('Название', max_length=255)
    users = models.ManyToManyField(User, related_name="interests")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name        = 'Интерес'
        verbose_name_plural = 'Интересы'


class Result(models.Model):
    """"""
    users   = models.ManyToManyField(User, related_name="results")
    request = models.CharField(max_length=1000)
    result  = models.CharField(max_length=5000)
    created = models.DateTimeField(auto_now_add=True)
    tools   = models.ManyToManyField('Tool', related_name="results", blank=True)

    class Meta:
        verbose_name        = 'Результат'
        verbose_name_plural = 'Резултаты'

    def __str__(self):
        return self.request[:10]


class Tool(models.Model):
    class Status(models.TextChoices):
     # Actual value ↓      # ↓ Displayed on Django Admin  
        TEXT     = 'Text', _('Text')
        DOCUMENT = 'Document', _('Document')
        LINK     = 'Link', _('Link')
    notes  = models.CharField('примечания', max_length=255)
    status = models.BooleanField(default=False)
    energy = models.PositiveIntegerField(_('Energy'), default=0)
    type   = models.CharField('Тип', choices=Status.choices, max_length=10)

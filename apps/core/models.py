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
        verbose_name_plural = 'Результаты'

    def __str__(self):
        return self.request


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

    class Meta:
        verbose_name        = 'Tool'
        verbose_name_plural = 'Tools'

    def __str__(self):
        return f'{self.notes}|{self.status}|{self.energy}|{self.type}'


class Privacy(models.Model):
    """Соглашаения юзера"""
    qmonth    = models.CharField('Qmonth', max_length=255)
    lifetime  = models.CharField('Data lifetime', max_length=255)
    reg_date  = models.BooleanField('Account registration date', default=False)
    email     = models.BooleanField('Email', default=False)
    payments  = models.BooleanField('Payments', default=False)
    sessions  = models.BooleanField('IP sessions', default=False)
    tg_info   = models.BooleanField('Telegram username/id', default=False)
    username  = models.BooleanField('Username', default=False)
    location  = models.BooleanField('Location', default=False)
    dob       = models.BooleanField('Date of Birth', default=False)
    full_name = models.BooleanField('Name and Surname', default=False)
    api_keys  = models.BooleanField('Keys for authorization on third-party services', default=False)
    public_keys     = models.BooleanField('WEB3 public keys', default=False)
    voice_recording = models.BooleanField('Voice recordings', default=False)
    personal_media  = models.BooleanField('Personal photos/videos', default=False)
    user            = models.OneToOneField(User, on_delete=models.CASCADE, related_name="privacy")

    class Meta:
        verbose_name        = 'Privacy'
        verbose_name_plural = 'Privacy'

    def __str__(self):
        return self.qmonth
    

class WhiteList(models.Model):
    """"""
    name           = models.CharField('Name', max_length=255)
    specialization = models.CharField('Specialization', max_length=255)
    organization   = models.CharField('Organization', max_length=255)
    email          = models.EmailField('Email', max_length=255)
    notes          = models.CharField('Notes', max_length=255)
    status         = models.CharField('Status', max_length=255)
    created        = models.DateTimeField(auto_now_add=True)
    user           = models.OneToOneField(User, on_delete=models.CASCADE, 
                                          related_name="white_list")


    class Meta:
        verbose_name        = 'White List'
        verbose_name_plural = 'White Lists'

    def __str__(self):
        return self.name
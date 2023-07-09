from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail

from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import random

from .managers import UserManager


def user_directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/avatars/user_<id>/<filename>
        return "avatars/user_{0}/{1}".format(instance.id, filename)


class User(AbstractBaseUser, PermissionsMixin):
    """AbstractCustomUser
    """ 
    username    = None
    email       = models.EmailField(_('email address'), unique=True)
    tg_username = models.CharField(_('telegramm name'), max_length=255, blank=True)
    tg_id       = models.CharField(_('telegramm id'), max_length=255, blank=True)
    created     = models.DateTimeField(_("date created"), default=timezone.now)
    dob         = models.DateTimeField(_("date of birthday"), blank=True, null=True)
    otp         = models.CharField(max_length=6, null=True, blank=True)
    energy      = models.PositiveIntegerField(_('Energy'), default=0)
    kyc         = models.BooleanField(_("kyc"), default=False)
    location    = models.CharField(_('city'), max_length=255, blank=True)
    language    = models.CharField(_('language'), max_length=255, blank=True)
    mainkey     = models.CharField(_('main key'), max_length=255, blank=True)
    tariff      = models.ForeignKey('tariffs.Tariff', on_delete=models.SET_NULL, 
                                    related_name='users', null=True, blank=True)
    avatar      = models.ImageField(
                                upload_to=user_directory_path, 
                                height_field=None,
                                width_field=None, 
                                null=True, blank=True
                            )
    is_staff    = models.BooleanField(
                                _("staff status"),
                                default=False,
                                help_text=_("Designates whether the user can log into this admin site."),
                            )
    is_active   = models.BooleanField(
                                _("active"),
                                default=False,
                                help_text=_(
                                    "Designates whether this user should be treated as active. "
                                    "Unselect this instead of deleting accounts."
                                ),
                            )
    
    objects = UserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return f"{self.email}"
    
    def get_full_name(self):
        return f"{self.email}"
    
    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_short_name(self):
        """Return the short name for the user."""
        return self.tg_username

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


    def save(self, *args, **kwargs):
        number_list = [x for x in range(10)]  # Use of list comprehension
        code_items_for_otp = []

        for i in range(6):
            num = random.choice(number_list)
            code_items_for_otp.append(num)

        code_string = "".join(str(item)
                                        for item in code_items_for_otp)  # list comprehension again
        # A six digit random number from the list will be saved in top field
        self.otp = code_string
        super().save(*args, **kwargs)
    

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


from django.contrib.auth.base_user import BaseUserManager
from django.core.mail import send_mail
from django.conf import settings


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email=None, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            **extra_fields
        )
        # проверяем является ли пользователь
        # суперпользователем
        if extra_fields.get('is_superuser'):
            user = self.model(
                email=email,
                **extra_fields
            )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', False)
        self_create = self._create_user(email=email, password=password, **extra_fields)

        if self_create.email != None:
            send_mail(
                subject=f'Привет! {self_create.email}',
                message=f'Код для активации аккаунта: {self_create.otp}',
                from_email='noreply@church.com',
                recipient_list=[self_create.email,]
            )
            
        return self_create
    

    def create_superuser(self, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(
            password=password,
            **extra_fields
        )
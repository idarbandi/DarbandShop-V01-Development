from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django_countries.fields import CountryField


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, user_name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_superuser', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('super user must be assigned to isstaff=True.')

        if other_fields.get('is_superuser') is not True:
            raise ValueError('super user must be assigned to issuperuser=True.')

        return self.create_user(email, user_name, password, **other_fields)

    def create_user(self, email, user_name, password, **other_fields):
        if not email:
            raise ValueError(_('You Must Provide an Email Address'))
        email = self.normalize_email(email)
        user = self.model(user_name=user_name, email=email,
                          **other_fields)
        user.set_password(password)
        user.save()
        return user


class UserBase(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('Email Address'), unique=True)
    user_name = models.CharField(_('user name'), max_length=150, unique=True)
    first_name = models.CharField(_('first name'), max_length=20, blank=True)
    start_date = models.DateTimeField(_('user join date'), auto_now_add=True)
    about = models.TextField(_('about user'), blank=True)
    # Delivery Deatil
    country = CountryField()
    phone_number = models.CharField(max_length=15, blank=True)
    post_code = models.CharField(max_length=12, blank=True)
    address_line_1 = models.CharField(max_length=15, blank=True)
    address_line_2 = models.CharField(max_length=15, blank=True)
    own_city = models.CharField(max_length=15, blank=True)
    # User Status
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name']

    def __str__(self):
        return self.user_name

    class Meta:
        verbose_name = _('Accounts')
        verbose_name_plural = _('Accounts')

    def email_user(self, subject, message):
        send_mail(
            subject,
            message,
            "1@1.com",
            [self.email],
            fail_silently=False
        )

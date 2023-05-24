from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django_countries.fields import CountryField
import uuid


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_superuser', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('super user must be assigned to isstaff=True.')

        if other_fields.get('is_superuser') is not True:
            raise ValueError('super user must be assigned to issuperuser=True.')

        return self.create_user(email, name, password, **other_fields)

    def create_user(self, email, name, password, **other_fields):
        if not email:
            raise ValueError(_('You Must Provide an Email Address'))
        email = self.normalize_email(email)
        user = self.model(name=name, email=email,
                          **other_fields)
        user.set_password(password)
        user.save()
        return user


class Customer(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('Email Address'), unique=True)
    name = models.CharField(_('user name'), max_length=150)
    mobile = models.CharField(_('first name'), max_length=20, blank=True)
    # User Status
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name

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

class Address(models.Model):
    """
        Address Table
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer_id = models.ForeignKey(Customer, verbose_name=_("customer"), on_delete=models.CASCADE)
    # Delivery Deatil
    country = CountryField()
    phone_number = models.CharField(max_length=15, blank=True)
    post_code = models.CharField(max_length=12, blank=True)
    address_line_1 = models.CharField(max_length=15, blank=True)
    address_line_2 = models.CharField(max_length=15, blank=True)
    town_city = models.CharField(max_length=15, blank=True)
    delivery_instructions = models.CharField(_("Delivery Instructions"), max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    default = models.BooleanField(_("Default"), default=False)
    
    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Adresses")
        
    def __str__(self):
        return _("Address")
    
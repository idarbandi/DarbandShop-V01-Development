from django.db import models
from django.utils.translation import gettext_lazy as _


class DeliveryOptions(models.Model):
    """
        The Delivery Methods Table Containing All Deliveries
    """
    Delivery_Choices = [
        ("IS", "In Store"),
        ("HD", "Home Delivery"),
        ("DD", "Digital Delivery"),
    ]

    delivery_name = models.CharField(max_length=255, verbose_name=_("delivery_name"), help_text=_("Required"))
    delivery_price = models.DecimalField(
        verbose_name=_("Delivery Price"),
        help_text=_("Maximum 999.99"),
        error_messages={
            "name": {
                "max_length": _("The Price Must Be Between 0 and 999.99")
            }
        },
        max_digits=5,
        decimal_places=2
    )
    delivery_method = models.CharField(
        choices=Delivery_Choices,
        verbose_name=_("Delivery_methods"),
        help_text=_("Required"),
        max_length=255
    )
    delivery_timeframe = models.CharField(
        verbose_name=_("delivery timeframe"),
        help_text=_("Required"),
        max_length=255
    )
    delivery_window = models.CharField(
        verbose_name=_("delivery window"),
        help_text=_("Required"),
        max_length=255
    )
    order = models.IntegerField(verbose_name=_("list order"), help_text=_("Required"), default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = _("Delivery Option")
        verbose_name_plural = _("Delivery Options")
        
    def __str__(self):
        return self.delivery_name
    

class PaymentSelections(models.Model):
    """
        Store Payment Options
    """
    name = models.CharField(
        verbose_name=_("name"),
        help_text=_("Required"),
        max_length=255
    )
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = _("Payment Selection")
        verbose_name_plural = _("Payment Selections")
    
    def __str__(self):
        return self.name
    

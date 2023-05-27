from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth import settings


class Category(MPTTModel):
    """
        Category Table Implemented with MPTT
    """
    name = models.CharField(
        verbose_name=_("Category Name"),
        help_text=_("Required & Unique"),
        max_length=255,
        unique=True
    )
    slug = models.SlugField(
        verbose_name=_("Category Safe URL"),
        max_length=255,
        unique=True
    )
    parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")
    is_active = models.BooleanField(default=True)

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def get_absolute_url(self):
        return reverse("store:category_list", args=[self.slug])

    def __str__(self):
        return self.name


class ProductType(models.Model):
    """
        Will Provide a List Of Different types of products That are For The Sale
    """
    name = models.CharField(verbose_name=_("Product Name"), help_text=_("Required"), max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Product Type")
        verbose_name_plural = _("Product Types")

    def __str__(self):
        return self.name


class ProductSpecification(models.Model):
    """
        Contains Products Specification or Feature For The Product Types
    """
    product_type = models.ForeignKey(ProductType, on_delete=models.RESTRICT)
    name = models.CharField(verbose_name=_("Name"), help_text=_("Required"), max_length=255)

    class Meta:
        verbose_name = _("Product Specification")
        verbose_name_plural = _("Product Specifications")

    def __str__(self):
        return self.name


class Product(models.Model):
    """
        The Product Tabel Containing All Product Items
    """
    product_type = models.ForeignKey(ProductType, on_delete=models.RESTRICT)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    title = models.CharField(
        verbose_name=_("title"),
        help_text=_("required"),
        max_length=255
    )
    description = models.TextField(verbose_name=_("Description"), help_text=_("Not Required"), blank=True)
    slug = models.SlugField(max_length=255)
    regular_price = models.DecimalField(
        verbose_name=_('Regular Price'),
        help_text=_("Maximum 999.99"),
        error_messages={
            "name": {
                "max_length": _("The Price must Be Between 0 and 999.99")
            },
        },
        max_digits=5,
        decimal_places=2
    )
    discount_price = models.DecimalField(
        verbose_name=_('Discount Price'),
        help_text=_("Maximum 999.99"),
        error_messages={
            "name": {
                "max_length": _("The Price must Be Between 0 and 999.99")
            },
        },
        max_digits=5,
        decimal_places=2
    )
    is_active = models.BooleanField(
        verbose_name=_("Product Visibility"),
        help_text=_("Change Product Visibility"),
        default=True
    )
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    users_wishlist = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="user_wishlist", blank=True)
    
    def get_absolute_url(self):
        return reverse("store:product_detail", args=[self.slug])

    class Meta:
        ordering = ("-created_at", )
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return self.title


class ProductSpecificationValue(models.Model):
    """
        The Product Specification Value Table That holds Each Value Specifications or Bespoke Features
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    specification = models.ForeignKey(ProductSpecification, on_delete=models.RESTRICT)
    value = models.CharField(
        verbose_name=_("value"),
        help_text=_(" Product Specification Value (Maximum of 255 words)"),
        max_length=255
    )

    def __str__(self):
        return self.value


class ProductImage(models.Model):
    """
        The Products Images
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_image")
    image = models.ImageField(
        verbose_name=_("image"),
        help_text=_("Upload a Product Image"),
        upload_to="image/",
        default="image/default.png"
    )
    alt_text = models.CharField(
        verbose_name=_("Alternative Text"),
        help_text=_("Please Add Alternative Text"),
        max_length=255,
        null=True,
        blank=True
    )
    is_feature = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")

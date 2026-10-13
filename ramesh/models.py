from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
from django.db import models, transaction
from django.contrib.auth.models import User
from django.utils.text import slugify
import logging

from .validators import validate_image_upload


logger = logging.getLogger(__name__)


def delete_unreferenced_image(image_name):
    if not image_name:
        return
    if Product.objects.filter(image=image_name).exists():
        return
    if Profile.objects.filter(image=image_name).exists():
        return
    try:
        default_storage.delete(image_name)
    except OSError:
        logger.exception("Could not delete unreferenced image %s", image_name)


class Product(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170, unique=True, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True,
        validators=[validate_image_upload],
    )
    stock = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def clean(self):
        super().clean()
        if self.price < 0:
            raise ValidationError({'price': 'Price cannot be negative.'})
        if self.stock < 0:
            raise ValidationError({'stock': 'Stock cannot be negative.'})

    def save(self, *args, **kwargs):
        old_image_name = None
        should_check_old_image = kwargs.get('update_fields') is None or 'image' in kwargs['update_fields']
        if self.pk and should_check_old_image:
            old_image_name = type(self).objects.filter(pk=self.pk).values_list('image', flat=True).first()
        if not self.slug:
            self.slug = slugify(self.name)
        self.full_clean()
        result = super().save(*args, **kwargs)
        if old_image_name and old_image_name != self.image.name:
            transaction.on_commit(lambda: delete_unreferenced_image(old_image_name))
        return result

    def delete(self, *args, **kwargs):
        old_image_name = self.image.name if self.image else None
        result = super().delete(*args, **kwargs)
        if old_image_name:
            transaction.on_commit(lambda: delete_unreferenced_image(old_image_name))
        return result

    def __str__(self):
        return self.name


# Repair Model
class Repair(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    city = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# Order Model
class Order(models.Model):
    STATUS_CHOICES = [
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='orders',
    )

    product_name = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()

    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    reserved_quantity = models.PositiveIntegerField(default=0)

    order_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Processing')
    delivery_days = models.CharField(max_length=20, default='3-7 days')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.product_name}"


# Profile Model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='profile_images/',
        blank=True,
        null=True,
        validators=[validate_image_upload],
    )

    def __str__(self):
        return f"{self.user.username}'s profile"

    def save(self, *args, **kwargs):
        old_image_name = None
        should_check_old_image = kwargs.get('update_fields') is None or 'image' in kwargs['update_fields']
        if self.pk and should_check_old_image:
            old_image_name = type(self).objects.filter(pk=self.pk).values_list('image', flat=True).first()
        result = super().save(*args, **kwargs)
        if old_image_name and old_image_name != self.image.name:
            transaction.on_commit(lambda: delete_unreferenced_image(old_image_name))
        return result

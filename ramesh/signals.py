from django.db import transaction
from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import Profile, Product, delete_unreferenced_image


@receiver(post_delete, sender=Product, dispatch_uid='ramesh.delete_product_image')
@receiver(post_delete, sender=Profile, dispatch_uid='ramesh.delete_profile_image')
def schedule_deleted_image_cleanup(sender, instance, using, **kwargs):
    image_name = instance.image.name if instance.image else None
    if image_name:
        transaction.on_commit(
            lambda: delete_unreferenced_image(image_name, using=using),
            using=using,
        )

from django.db.models.signals import post_delete
from django.dispatch import receiver
from listings.models import Image
from listings.imagekit import destroy_image


@receiver(post_delete, sender=Image)
def delete_imagekit_image(sender, instance, **kwargs):
    if instance.storage_key:
        destroy_image(instance.storage_key)
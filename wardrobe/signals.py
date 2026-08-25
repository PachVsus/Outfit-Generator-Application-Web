from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from .models import Garment


def delete_file(field_file):
    if field_file and field_file.name:
        field_file.storage.delete(field_file.name)


@receiver(post_delete, sender=Garment)
def remove_deleted_garment_image(sender, instance, **kwargs):
    delete_file(instance.image)


@receiver(pre_save, sender=Garment)
def remove_replaced_garment_image(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        previous = sender.objects.only("image").get(pk=instance.pk)
    except sender.DoesNotExist:
        return
    if previous.image.name and previous.image.name != instance.image.name:
        delete_file(previous.image)

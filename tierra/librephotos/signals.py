import os

from django.db import models
from django.dispatch import receiver
from librephotos.models import Face, Person


@receiver(models.signals.post_delete, sender=Person)
def reset_person(sender, instance, **kwargs):
    instance.faces.update(person=Person.get_unknown_person(instance.cluster_owner))


# From: https://stackoverflow.com/questions/16041232/django-delete-filefield
@receiver(models.signals.post_delete, sender=Face)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

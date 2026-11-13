from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Actors

@receiver (post_delete,sender=Actors)
def delete_actor_portrait(sender,instance,**kwargs):

    if instance.portrait:
        instance.portrait.delete(save=False)
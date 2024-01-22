import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from relays.models import Message, MessageEmbed
from relays.tasks import process_embed, process_message

from .app_settings import (
    RELAYS_TASK_PRIORITY_PROCESSEMBED, RELAYS_TASK_PRIORITY_PROCESSMESSAGE,
)

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Message)
def message_new(sender, instance: Message, created: bool, *args, **kwargs):
    if created is True:
        process_message.apply_async(
            args=[instance.pk], priority=RELAYS_TASK_PRIORITY_PROCESSMESSAGE)
    else:
        return


@receiver(post_save, sender=MessageEmbed)
def embed_new(sender, instance: Message, created: bool, *args, **kwargs):
    if created is True:
        process_embed.apply_async(
            args=[instance.pk], priority=RELAYS_TASK_PRIORITY_PROCESSEMBED)
    else:
        return

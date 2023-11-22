from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

class Notification(models.Model):
    actor_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='actor')
    actor_object_id = models.PositiveIntegerField()
    actor = GenericForeignKey('actor_content_type', 'actor_object_id')

    verb = models.CharField(max_length=255)

    action_object_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='action_object', null=True, blank=True)
    action_object_object_id = models.PositiveIntegerField(null=True, blank=True)
    action_object = GenericForeignKey('action_object_content_type', 'action_object_object_id')

    target_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='target', null=True, blank=True)
    target_object_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey('target_content_type', 'target_object_id')

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.actor} {self.verb} {self.action_object} on {self.target}'


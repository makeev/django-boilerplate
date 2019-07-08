import os
from django.conf import settings
from django.db import models
from django.db.models.signals import pre_delete, post_save
from django.dispatch.dispatcher import receiver


class MediaFile(models.Model):
    file = models.FileField(upload_to='files')
    size_bytes = models.PositiveIntegerField(null=True, default=0, editable=False)
    description = models.CharField(max_length=300, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        if self.file and self.file.name:
            return self.file.name


@receiver(pre_delete, sender=MediaFile)
def mymodel_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.file.delete(False)


@receiver(post_save, sender=MediaFile)
def notify(sender, instance, created, update_fields, **kwargs):
    if update_fields and 'size_bytes' in update_fields:
        # чекаем это поле чтобы не упасть в рекурсию
        return False

    if not instance.file or not instance.file.name:
        # ну вдруг...
        return False

    filepath = '%s/%s' % (settings.MEDIA_ROOT, instance.file.name)
    if os.path.exists(filepath):
        instance.size_bytes = os.path.getsize(filepath)
        instance.save(update_fields=['size_bytes'])

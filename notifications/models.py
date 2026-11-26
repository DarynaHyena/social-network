from django.db import models
from django.conf import settings


class Notification(models.Model):

    class NotificationType(models.TextChoices):
        LIKE = 'like', 'Лайк'
        SHARE = 'share', 'Репост'
        COMMENT = 'comment', 'Коментар'
        COMMUNITY_JOIN = 'community_join', 'Вступ до спільноти'

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_notifications'
    )

    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_notifications'
    )

    notification_type = models.CharField(
        max_length=30,
        choices=NotificationType.choices
    )

    post = models.ForeignKey(
        'posts.Posts',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='notifications'
    )

    community = models.ForeignKey(
        'communities.Community',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='notifications'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Сповіщення'
        verbose_name_plural = 'Сповіщення'

    def str(self):
        return (
            f'{self.actor} → {self.recipient}: '
            f'{self.get_notification_type_display()}'
        )
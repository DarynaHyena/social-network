from django.db import models
from settings.settings import AUTH_USER_MODEL
from pathlib import Path
from django.conf import settings



# Клас для спільнот
class Community(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Назва")
    description = models.TextField(blank=True, verbose_name="Опис")
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="owned_communities", verbose_name="Власник", null=True, blank=True)
    media = models.FileField(upload_to='posts/', blank=True, null=True, verbose_name="Файли")

    @property
    def extension(self):
        return Path(self.media.name).suffix.lower()
    @property
    def is_image(self):
        return self.extension in [".jpg", ".jpeg", ".png", ".gif", ".webp"]
    @property
    def is_video(self):
        return self.extension in [".mp4", ".webm", ".mov"]
    @property
    def is_audio(self):
        return self.extension in [".mp3", ".wav", ".ogg"]

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Спільнота"
        verbose_name_plural = "Спільноти"

    def __str__(self):
        return self.name



# Клас для членства спільнот
class CommunityMembership(models.Model):

    class MembershipRole(models.TextChoices):
        MEMBER = 'member'
        MODERATOR = 'moderator'

    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='memberships')
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='community_memberships')
    role = models.CharField(max_length=20, choices=MembershipRole.choices, default=MembershipRole.MEMBER)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['community', 'user'], name='unique_community_member')]

        verbose_name = 'Учасник спільноти'
        verbose_name_plural = 'Учасники спільнот'

    def str(self):
        return f'{self.user.username} — {self.community.name}'
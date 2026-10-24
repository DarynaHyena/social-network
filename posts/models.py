from django.db import models
from settings.settings import AUTH_USER_MODEL
from communities.models import Community

# клас для постів
class Posts(models.Model):
    title = models.CharField(max_length=200, verbose_name='Назва')
    content = models.TextField(blank=True, null=True, verbose_name='Вміст')
    author = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts', verbose_name='Автор')
    community = models.ForeignKey(Community, on_delete=models.CASCADE,  related_name='posts',verbose_name='Спільнота')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Допис'
        verbose_name_plural = 'Дописи'

    def __str__(self):
        return f"{self.pk} {self.title} - {self.author.username}"


#клас для коментарів
class Comment(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='comments', verbose_name='Допис')
    author = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments', verbose_name='Автор')
    content = models.TextField(verbose_name='Вміст')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Коментар'
        verbose_name_plural = 'Коментарі'

    def __str__(self):
        return f" Comment by {self.pk}"

#клас для збереження лайків
class Like(models.Model):

    class VoteValue(models.IntegerChoices):
        LIKE = 1, 'Лайк'
        DISLIKE = -1, 'Дизлайк'

    post_item = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='likes', verbose_name='Допис')
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes', verbose_name='Користувач')
    vote = models.SmallIntegerField(choices=VoteValue.choices, verbose_name='Голос')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('post_item', 'user')
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'


#клас для збереження репостів
class Share(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="shares", verbose_name="Користувач")
    post = models.ForeignKey(Posts, on_delete=models.CASCADE,related_name="shares",verbose_name="Допис")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "post"],
                name="unique_user_post_share",
            )
        ]

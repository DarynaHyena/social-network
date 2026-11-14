from django.db.models import Count, Q, OuterRef, Subquery, IntegerField
from posts.models import Like


# Міксін для підрахунку статистики постів
class PostStatsMixin:
    def get_queryset(self):
        queryset = super().get_queryset()

        queryset = queryset.annotate(
            likes_count=Count(
                'likes',
                filter=Q(likes__vote=1),
                distinct=True
            ),
            dislikes_count=Count(
                'likes',
                filter=Q(likes__vote=-1),
                distinct=True
            ),
            shares_count=Count(
                'shares',
                distinct=True
            )
        )

        if self.request.user.is_authenticated:
            user_vote = Like.objects.filter(
                post_item=OuterRef('pk'),
                user=self.request.user
            ).values('vote')[:1]

            queryset = queryset.annotate(
                user_vote=Subquery(
                    user_vote,
                    output_field=IntegerField()
                )
            )

        return queryset
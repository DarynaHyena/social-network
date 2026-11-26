from django.db.models import Count, Q, OuterRef, Subquery, IntegerField, Max, Exists, BooleanField
from django.db.models.functions import Coalesce
from posts.models import Like, Share


class PostStatsMixin:
    """Adds reaction/repost counters and the current user's state to post querysets."""

    def get_queryset(self):
        queryset = super().get_queryset()

        queryset = queryset.annotate(
            likes_count=Count('likes', filter=Q(likes__vote=Like.VoteValue.LIKE), distinct=True),
            dislikes_count=Count('likes', filter=Q(likes__vote=Like.VoteValue.DISLIKE), distinct=True),
            shares_count=Count('shares', distinct=True),
            last_shared_at=Max('shares__created_at'),
        ).order_by(Coalesce('last_shared_at', 'created_at').desc(), '-created_at')

        if self.request.user.is_authenticated:
            user_vote = Like.objects.filter(
                post_item=OuterRef('pk'), user=self.request.user
            ).values('vote')[:1]
            user_share = Share.objects.filter(
                post=OuterRef('pk'), user=self.request.user
            )
            queryset = queryset.annotate(
                user_vote=Subquery(user_vote, output_field=IntegerField()),
                user_shared=Exists(user_share, output_field=BooleanField()),
            )

        return queryset

from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages

from .models import Notification


class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'notifications/list.html'
    context_object_name = 'notifications'
    paginate_by = 20

    def get_queryset(self):
        return (
            Notification.objects
            .filter(recipient=self.request.user)
            .select_related('actor', 'post', 'community')
            .order_by('-created_at')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['unread_count'] = Notification.objects.filter(
            recipient=self.request.user,
            is_read=False
        ).count()

        return context


@login_required
@require_POST
def mark_notification_read(request, pk):
    notification = get_object_or_404(
        Notification,
        pk=pk,
        recipient=request.user
    )

    notification.is_read = True
    notification.save(update_fields=['is_read'])

    if notification.post_id:
        return redirect('post-detail', pk=notification.post_id)

    if notification.community_id:
        return redirect(
            'community-detail',
            pk=notification.community_id
        )

    return redirect('notifications-list')


@login_required
@require_POST
def mark_all_read(request):
    Notification.objects.filter(
        recipient=request.user,
        is_read=False
    ).update(is_read=True)

    messages.success(
        request,
        'Усі сповіщення позначено як прочитані.'
    )

    return redirect('notifications-list')

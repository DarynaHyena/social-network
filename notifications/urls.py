from django.urls import path
from notifications import views

urlpatterns = [
    path('', views.NotificationListView.as_view(), name='notifications-list'),
    path('<int:pk>/read/', views.mark_notification_read, name='notification-read'),
    path('read-all/', views.mark_all_read, name='notifications-read-all'),
]
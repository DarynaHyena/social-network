from django.urls import path
from communities import views

urlpatterns = [
    # urls для спільнот
    path('', views.CommunityListView.as_view(), name='community-list'),
    path('detail/<int:pk>/', views.CommunityDetailView.as_view(), name='community-detail'),
    path('create/', views.CommunityCreateView.as_view(), name='community-create'),
    path('update/<int:pk>/', views.CommunityUpdateView.as_view(), name='community-update'),
    path('delete/<int:pk>/', views.CommunityDeleteView.as_view(), name='community-delete'),

    # urls для приєднання та виходу зі спільнот
    path('<int:pk>/join/', views.join_community, name='community-join'),
    path('<int:pk>/leave/', views.leave_community, name='community-leave'),
]
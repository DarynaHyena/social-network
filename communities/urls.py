from django.urls import path
from communities import views

urlpatterns = [
    path('', views.CommunityListView.as_view(), name='community-list'),
    path('detail/<int:pk>/', views.CommunityDetailView.as_view(), name='community-detail'),
    path('create/', views.CommunityCreateView.as_view(), name='community-create'),
    path('update/<int:pk>/', views.CommunityUpdateView.as_view(), name='community-update'),
    path('delete/<int:pk>/', views.CommunityDeleteView.as_view(), name='community-delete'),
]
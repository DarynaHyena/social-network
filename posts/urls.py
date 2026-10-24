from django.urls import path
from posts import views

urlpatterns = [
    # urls для постів
    path('', views.PostListView.as_view(), name='post-list'),
    path('detail/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('create/', views.PostCreateView.as_view(), name='post-create'),
    path('update/<int:pk>/', views.PostUpdateView.as_view(), name='post-update'),
    path('delete/<int:pk>/', views.PostDeleteView.as_view(), name='post-delete'),

    # urls для коментарів
    path("<int:post_pk>/comment/create/", views.CommentCreateView.as_view(), name="comment-create"),
    path('comment/update/<int:pk>/', views.CommentUpdateView.as_view(), name='comment-update'),
    path('comment/delete/<int:pk>/', views.CommentDeleteView.as_view(), name='comment-delete'),
]

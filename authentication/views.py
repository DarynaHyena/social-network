from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from .forms import CustomUserCreationForm, UserProfileForm
from django.contrib import messages
from django.db.models import Q, Count
from .models import CustomUser
from posts.models import Posts, Comment, Like, Share


class RegisterView(CreateView):
    template_name = 'authentication/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'authentication/edit_profile.html'
    form_class = UserProfileForm
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        messages.success(
            self.request,
            'Зміни профілю успішно збережено.'
        )
        return super().form_valid(form)
    

class PublicProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'authentication/public_profile.html'
    context_object_name = 'user_profile'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return get_object_or_404(CustomUser, username=self.kwargs.get('username'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = self.get_object()
        posts = Posts.objects.filter(author=user_profile).select_related('author', 'community').order_by('-created_at')

        context['posts'] = posts
        context['posts_count'] = posts.count()
        context['likes_count'] = Like.objects.filter(post_item__author=user_profile, vote=Like.VoteValue.LIKE).count()
        context['shares_count'] = Share.objects.filter(post__author=user_profile).count()
        context['comments_count'] = Comment.objects.filter(post__author=user_profile).count()
        context['communities_count'] = (user_profile.community_memberships.count())
        context['owned_communities_count'] = (user_profile.owned_communities.count())

        return context
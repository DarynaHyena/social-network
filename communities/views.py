from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from communities.models import Community
from communities.forms import CommunityForm
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse


def index(request):
    communities = Community.objects.all().order_by('name')
    paginator = Paginator(communities, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'communities/list.html', {'communities': communities, 'page_obj': page_obj})


class CommunityListView(ListView):
    model = Community
    context_object_name = 'communities'
    template_name = 'communities/list.html'
    paginate_by = 5


class CommunityCreateView(LoginRequiredMixin, CreateView):
    form_class = CommunityForm
    template_name = 'communities/form.html'
    model = Community

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("community-detail", kwargs={"pk": self.object.pk})


class CommunityUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Community
    form_class = CommunityForm
    template_name = 'communities/form.html'
    success_url = reverse_lazy("community-list")

    def test_func(self):
        community = self.get_object()
        return self.request.user == community.owner or self.request.user.role in ['admin']

    def get_success_url(self):
        return reverse("community-detail", kwargs={"pk": self.object.pk})


class CommunityDetailView(DetailView):
    model = Community
    context_object_name = 'community'
    template_name = 'communities/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = self.object.posts.all()
        return context


class CommunityDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Community
    template_name = 'communities/delete.html'
    success_url = reverse_lazy("community-list")

    def test_func(self):
        community = self.get_object()
        return self.request.user == community.owner or self.request.user.role in ['admin']
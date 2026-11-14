from multiprocessing import context
from urllib import response

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from communities.models import Community, CommunityMembership
from communities.forms import CommunityForm
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST



def index(request):
    communities = Community.objects.all().order_by('name')
    paginator = Paginator(communities, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'communities/list.html', {'communities': communities, 'page_obj': page_obj})



# Класи в'юшок для спільнот
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
        response = super().form_valid(form)
        CommunityMembership.objects.get_or_create(community=self.object, user=self.request.user, defaults={'role': CommunityMembership.MembershipRole.MODERATOR})

        return response

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

        if self.request.user.is_authenticated:
            context['is_member'] = (self.object.memberships.filter(user=self.request.user).exists() or self.object.owner_id == self.request.user.id)
        else:
            context['is_member'] = False

        context['members_count'] = self.object.memberships.count()

        return context


class CommunityDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Community
    template_name = 'communities/delete.html'
    success_url = reverse_lazy("community-list")

    def test_func(self):
        community = self.get_object()
        return self.request.user == community.owner or self.request.user.role in ['admin']




# В'юшок для членства спільнот
@login_required
@require_POST
def join_community(request, pk):
    community = get_object_or_404(Community, pk=pk)
    CommunityMembership.objects.get_or_create(community=community, user=request.user)

    return redirect('community-detail', pk=community.pk)


@login_required
@require_POST
def leave_community(request, pk):
    community = get_object_or_404(Community, pk=pk)

    # Власник не може вийти зі своєї спільноти
    if community.owner_id == request.user.id:
        return redirect('community-detail', pk=community.pk)

    CommunityMembership.objects.filter(community=community, user=request.user).delete()

    return redirect('community-detail', pk=community.pk)
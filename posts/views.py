from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from posts.models import Posts, Comment, Like, Share
from django.urls import reverse_lazy, reverse
from posts.forms import PostForm, CommentForm
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils.http import url_has_allowed_host_and_scheme
from posts.mixins import PostStatsMixin
from communities.models import CommunityMembership




# В'юшки для постів
def index(request):
    posts = Posts.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'posts/list.html', {'posts': posts, 'page_obj': page_obj})


class PostListView(PostStatsMixin, ListView):
    model = Posts
    context_object_name = 'posts'
    template_name = 'posts/list.html'
    paginate_by = 5


class PostCreateView(LoginRequiredMixin, CreateView):
    form_class = PostForm
    template_name = 'posts/form.html'
    model = Posts

    def form_valid(self, form):
        community = form.cleaned_data['community']
        user = self.request.user
        is_member = CommunityMembership.objects.filter(community=community, user=user).exists()
        if community.owner_id == user.id:
            CommunityMembership.objects.get_or_create(community=community,vuser=user, defaults={'role': CommunityMembership.MembershipRole.MODERATOR})
            is_member = True

        if not is_member:
            form.add_error('community', 'Щоб публікувати дописи, потрібно приєднатися до спільноти.')
            return self.form_invalid(form)

        form.instance.author = user

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("post-detail", kwargs={"pk": self.object.pk})
    
    
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Posts
    form_class = PostForm
    template_name = 'posts/form.html'
    success_url = reverse_lazy("post-list")

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author or self.request.user.role in ['admin']

    def get_success_url(self):
        return reverse("post-detail", kwargs={"pk": self.object.pk})
    

class PostDetailView(PostStatsMixin, DetailView):
    model = Posts
    context_object_name = 'post'
    template_name = 'posts/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()
        return context


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Posts
    template_name = 'posts/delete.html'
    success_url = reverse_lazy("post-list")

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author or self.request.user.role in ['admin']






# В'юшки для коментарів
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "comments/form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Posts, pk=self.kwargs['post_pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("post-detail", kwargs={"pk": self.object.post.pk})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comments/form.html'

    def test_func(self):
        comment = self.get_object()
        user = self.request.user
        
        return user == comment.author or user.role == 'admin'

    # def test_func(self):
    #     post = self.get_object()
    #     return self.request.user == post.creator or self.request.user.role in ['admin']

    def get_success_url(self):
        return reverse("post-detail", kwargs={"pk": self.object.post_id})
    

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'comments/delete.html'

    def test_func(self):
        comment = self.get_object()
        user = self.request.user
        return user == comment.author or user.role in ['admin']

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk':self.object.post_id})





# В'юшки для лайків, дизлайків та репостів
def get_return_url(request, post):
    url = request.POST.get('next')

    if url and url_has_allowed_host_and_scheme(
        url,
        allowed_hosts={request.get_host()}
    ):
        return redirect(url)

    return redirect('post-detail', pk=post.pk)


@login_required
@require_POST
def like_post(request, pk):
    post = get_object_or_404(Posts, pk=pk)

    reaction, created = Like.objects.get_or_create(
        post_item=post,
        user=request.user,
        defaults={'vote': Like.VoteValue.LIKE}
    )

    if not created:
        if reaction.vote == Like.VoteValue.LIKE:
            reaction.delete()
        else:
            reaction.vote = Like.VoteValue.LIKE
            reaction.save()

    return get_return_url(request, post)


@login_required
@require_POST
def dislike_post(request, pk):
    post = get_object_or_404(Posts, pk=pk)

    reaction, created = Like.objects.get_or_create(
        post_item=post,
        user=request.user,
        defaults={'vote': Like.VoteValue.DISLIKE}
    )

    if not created:
        if reaction.vote == Like.VoteValue.DISLIKE:
            reaction.delete()
        else:
            reaction.vote = Like.VoteValue.DISLIKE
            reaction.save()

    return get_return_url(request, post)


@login_required
@require_POST
def share_post(request, pk):
    post = get_object_or_404(Posts, pk=pk)

    share, created = Share.objects.get_or_create(
        post=post,
        user=request.user
    )

    if not created:
        share.delete()

    return get_return_url(request, post)

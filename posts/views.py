from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from posts.models import Posts, Comment, Like
from django.urls import reverse_lazy, reverse
from posts.forms import PostForm, CommentForm
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin



# В'юшки для постів
def index(request):
    posts = Posts.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'posts/list.html', {'posts': posts, 'page_obj': page_obj})


class PostListView(ListView):
    model = Posts
    context_object_name = 'posts'
    template_name = 'posts/list.html'
    paginate_by = 5


class PostCreateView(LoginRequiredMixin, CreateView):
    form_class = PostForm
    template_name = 'posts/form.html'
    model = Posts


    def form_valid(self, form):
        form.instance.author = self.request.user
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
        return self.request.user == post.creator or self.request.user.role in ['admin']

    def get_success_url(self):
        return reverse("post-detail", kwargs={"pk": self.object.pk})
    

class PostDetailView(DetailView):
    model = Posts
    context_object_name = 'post'
    template_name = 'posts/detail.html'


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Posts
    template_name = 'posts/delete.html'
    success_url = reverse_lazy("post-list")

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.creator or self.request.user.role in ['admin']






# В'юшки для коментарів
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "comments/form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.post_object
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("post-detail", kwargs={"pk": self.post_object.pk})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comments/form.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.creator or self.request.user.role in ['admin']

    def get_success_url(self):
        return reverse("post-detail", kwargs={"pk": self.object.post_id})
    

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'comments/delete.html'

    def test_func(self):
        comment = self.get_object()
        user = self.request.user
        return user == comment.creator or user.role in ['admin']

    def get_success_url(self):
        return reverse('task-detail', kwargs={'pk':self.object.task_id})

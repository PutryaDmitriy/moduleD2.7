from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import resolve
from django.shortcuts import redirect
from django.core.mail import EmailMultiAlternatives
from django.views import View
from django.contrib.auth.models import Group

from django.template.loader import render_to_string

from .models import Post, Category, PostCategory, User, Author
from .filters import PostFilter
from .forms import PostForm
from django.conf import settings
DEFAULT_FROM_EMAIL = settings.DEFAULT_FROM_EMAIL

class PostList(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-pub_date')
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context

class PostDetail(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
# Create your views here.

class PostSearch(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'search'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


class CreatePostView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'add.html'
    form_class = PostForm
    permission_required = ('news.add_post',)

class UpdatePostView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'edit.html'
    form_class = PostForm
    permission_required = ('news.change_post',)

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class DeletePostView(LoginRequiredMixin, DeleteView):
    template_name = 'delete.html'
    queryset = Post.objects.all()
    success_url = '/'

class CategoryPostList(ListView):
    model = Post
    template_name = 'category/category_posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        self.id = resolve(self.request.path_info).kwargs['pk']
        cat = Category.objects.get(id=self.id)
        queryset = Post.objects.filter(category=cat).order_by('-pub_date')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        category = Category.objects.get(id=self.id)
        subscribed = category.subscribers.filter(email=user.email)
        context['category'] = category
        if subscribed:
            context['subscribed'] = 1
        return context

def subscribe_to_category(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    if not category.subscribers.filter(id=user.id).exists():
        email = user.email
        category.subscribers.add(user)
        html = render_to_string(
            'subscribe/subscriber.html',
            {
                'category': category,
                'user': user,
            }
        )

        msg = EmailMultiAlternatives(
            subject=f'{category} subscribe',
            from_email=DEFAULT_FROM_EMAIL,
            body='',
            to=[email,],
        )
        msg.attach_alternative(html, 'text/html')
        msg.send()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect(request.META.get('HTTP_REFERER'))

def unsubscribe_from_category(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    if category.subscribers.filter(id=user.id).exists():
        category.subscribers.remove(user)
        # html = render_to_string(
        #     'mail/subscriber',
        #     {
        #         'category': category,
        #         'user': user,
        #     }
        # )
        #
        # msg = EmailMultiAlternatives(
        #     subject=f'{category} subscribe',
        #     from_email='',
        #     body='',
        #     to=[email,]
        # )
        # msg.send()

    return redirect(request.META.get('HTTP_REFERER'))

class UserProfile(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'accounts/profile.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        categories = []
        for category in Category.objects.all():
            for subscribe in category.subscribers.all():
                if subscribe==user:
                    categories.append(category)
        context['categories'] = categories
        posts = {}
        for category in categories:
            posts[category]=[]
            for post in Post.objects.all():
                for cat in post.category.all():
                    if cat == category:
                        posts[category].append(post)
        context['posts'] = posts




        if not user.groups.filter(name='authors').exists():
            context['status'] = "Читатель"
            context['author_posts'] = None
        else:
            context['status'] = "Автор"
            author_posts = []
            for post in Post.objects.all():
                if str(post.author) == str(user):
                    author_posts.append(post)
            context['author_posts'] = author_posts
        return context

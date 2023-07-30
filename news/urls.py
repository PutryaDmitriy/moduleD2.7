from django.urls import path
from .views import PostList, PostDetail, PostSearch, CreatePostView, DeletePostView, UpdatePostView, CategoryPostList, subscribe_to_category, unsubscribe_from_category
from .views import UserProfile
from django.contrib.auth.views import LogoutView

app_name='news'

urlpatterns =[
    path('', PostList.as_view(), name='posts'),
    path('news/<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search', PostSearch.as_view()),
    path('add', CreatePostView.as_view(), name='post_create'),
    path('<int:pk>/edit/', UpdatePostView.as_view(), name='post_update'),
    path('<int:pk>/delete/', DeletePostView.as_view(), name='post_delete'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('categories/<int:pk>/', CategoryPostList.as_view(), name='category_posts'),
    path('subscribe/<int:pk>/', subscribe_to_category, name='subscribe'),
    path('unsubscribe/<int:pk>/', unsubscribe_from_category, name='unsubscribe'),
    path('profile/<int:pk>/', UserProfile.as_view(), name='profile'),
]


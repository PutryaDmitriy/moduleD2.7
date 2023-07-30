from django.db import models
from django.contrib.auth.models import User, Group
from datetime import datetime



# Create your models here.

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        posts_rating = 0
        posts = Post.objects.filter(author_id=self.user.id).values('rating')
        for post in posts:
            posts_rating += post['rating']

        comments_rating = 0
        author_comments = Comment.objects.filter(user_id=self.user.id).values('rating')
        for comment in author_comments:
            comments_rating += comment['rating']

        post_comments_rating = 0
        post_comments = Comment.objects.filter(user_id=self.user.id).values('rating')
        for comment in post_comments:
            post_comments_rating +=comment['rating']

        self.rating = posts_rating * 3 + comments_rating + post_comments_rating
        self.save()

    def __str__(self):
        return f'{self.user}'

class Category(models.Model):
    category = models.CharField(max_length=128, unique=True)
    subscribers = models.ManyToManyField(User, blank=True)
    def __str__(self):
        return f'{self.category}'

class Post(models.Model):
    artickle = 'ar'
    news = 'nw'
    TYPES = [
        (artickle, 'статья'),
        (news, 'новость')
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE, default=artickle)
    type = models.CharField(max_length=2, choices=TYPES, default=artickle)
    pub_date = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=250)
    content = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        # rating = self.rating
        self.rating -= 1 if self.rating > 0 else 0
        self.save()

    def preview(self):
        return self.content[:124] + "..."

    def get_absolute_url(self):
        return f'/news/{self.id}'

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        # rating = self.rating
        self.rating -= 1 if self.rating > 0 else 0
        self.save()


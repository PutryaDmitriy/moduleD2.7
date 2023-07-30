from django.contrib import admin
from .models import Post, Category

class PostAdmin(admin.ModelAdmin):
    fields = ('author', 'type', 'title', 'content', 'rating')

#
# class PostInline(admin.TabularInline):
#     model = PostCategory
#     extra = 1
#
# class PostAdmin(admin.ModelAdmin):
#     inlines = (PostInline, )
#
# class PostCategoryAdmin(admin.ModelAdmin):
#     inlines = (PostInline,)

admin.site.register(Post)
admin.site.register(Category)
# Register your models here.
# admin.site.register(PostCategory, PostAdmin)

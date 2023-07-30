from django_filters import FilterSet
from .models import Post, Author

class PostFilter(FilterSet):

    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'pub_date': ['date__gte'],
            'author': ['exact']
        }



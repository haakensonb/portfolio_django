from django.shortcuts import render

from .models import Post

def index(request):
    """
    Render part of all the posts by most recently created
    """
    latest_posts_list = Post.objects.order_by('-pub_date')
    context = {'latest_posts_list': latest_posts_list}
    return render(request, 'blog/index.html', context)

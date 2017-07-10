from django.shortcuts import render, get_object_or_404

from .models import Post


def index(request):
    """
    Render part of all the posts by most recently created
    """
    latest_posts_list = Post.objects.order_by('-pub_date')
    context = {'latest_posts_list': latest_posts_list}
    return render(request, 'blog/index.html', context)


def detail(request, post_id):
    """
    Render an individual post
    """
    post = get_object_or_404(Post, pk=post_id)
    context = {'post': post}
    return render(request, 'blog/detail.html', context)

from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .models import Post


def index(request):
    """
    Render part of all the posts by most recently created
    """
    # Only return posts that have been published in the past
    latest_posts_list = Post.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')
    context = {'latest_posts_list': latest_posts_list}
    return render(request, 'blog/index.html', context)


def detail(request, post_id):
    """
    Render an individual post that has a pub_date in the past
    """
    post = get_object_or_404(Post.objects.filter(pub_date__lte=timezone.now()), pk=post_id)
    context = {'post': post}
    return render(request, 'blog/detail.html', context)

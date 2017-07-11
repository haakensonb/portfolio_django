from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .models import Post, Tag


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
    # As of now latest_posts_list isn't needed in the detail view
    # because I want it to have a more minimal look.
    post = get_object_or_404(Post.objects.filter(pub_date__lte=timezone.now()), pk=post_id)
    context = {'post': post}
    return render(request, 'blog/detail.html', context)

def by_tag(request, tag_word):
    """
    Render all the posts with specified tag
    """
    # Get queryset of Tag object with correct word. Probably a better way to do this
    tag = Tag.objects.filter(word=tag_word)
    posts = Post.objects.filter(tags__in=tag).order_by('-pub_date')
    # Required for sidebar view. This doesn't seem right but as of now 
    # I don't know how to do this without repeating query in multiple views.
    latest_posts_list = Post.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')
    context = {'posts': posts, 'tag': tag, 'latest_posts_list': latest_posts_list}
    return render(request, 'blog/by_tag.html', context)

def archives(request, year, month):
    """
    Render all posts from specified year and month
    """
    posts = Post.objects.filter(pub_date__year=year, pub_date__month=month)
    latest_posts_list = Post.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')
    context = {'posts': posts, 'year': year, 'month': month, 'latest_posts_list': latest_posts_list}
    return render(request, 'blog/archives.html', context)

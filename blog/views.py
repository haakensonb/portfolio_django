from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Post, Tag


def index(request):
    """
    Render part of all the posts by most recently created
    """
    latest_posts_list = Post.objects.filter(
        pub_date__lte=timezone.now()).order_by('-pub_date')
    paginator = Paginator(latest_posts_list, 8)

    page = request.GET.get('page')
    try:
        paginated_posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        paginated_posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page
        paginated_posts = paginator.page(paginator.num_pages)

    context = {'paginated_posts': paginated_posts}
    return render(request, 'blog/index.html', context)


def detail(request, post_id):
    """
    Render an individual post that has a pub_date in the past
    """
    post = get_object_or_404(
        Post.objects.filter(pub_date__lte=timezone.now()), pk=post_id)
    context = {'post': post}
    return render(request, 'blog/detail.html', context)


def by_tag(request, tag_word):
    """
    Render all the posts with specified tag
    """
    # Get queryset of Tag object with correct word. Probably a better way to do this
    tag = Tag.objects.filter(word=tag_word)
    posts = Post.objects.filter(tags__in=tag).order_by('-pub_date')

    paginator = Paginator(posts, 8)

    page = request.GET.get('page')
    try:
        paginated_posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        paginated_posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page
        paginated_posts = paginator.page(paginator.num_pages)

    context = {'posts': posts, 'tag': tag, 'paginated_posts': paginated_posts}
    return render(request, 'blog/by_tag.html', context)


def archives(request, year, month):
    """
    Render all posts from specified year and month
    """
    posts = Post.objects.filter(pub_date__year=year, pub_date__month=month)

    paginator = Paginator(posts, 8)

    page = request.GET.get('page')
    try:
        paginated_posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        paginated_posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page
        paginated_posts = paginator.page(paginator.num_pages)

    context = {'posts': posts, 'year': year, 'month': month,'paginated_posts': paginated_posts}
    return render(request, 'blog/archives.html', context)

from django.utils import timezone

from .models import Post, Tag


def sidebar_processor(request):
    """
    Send latest_post_list and tags variables to every
    view so that the sidebar will work correctly.
    """
    # Only return posts that have been published in the past
    latest_posts_list = Post.objects.filter(
        pub_date__lte=timezone.now()).order_by('-pub_date')
    tags = Tag.objects.all()
    return {'latest_posts_list': latest_posts_list, 'tags': tags}

import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Post

def create_post(title, days):
    """
    Create a post with the given title name and published the
    the number of 'days' offset to now (negative for questions published
    in the past, positive for those that have yet to be published)
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Post.objects.create(title=title, body='test', pub_date=time)


class PostIndexViewTests(TestCase):
    def test_no_posts(self):
        """
        If no posts exist, latest_posts_lists returns empty
        """
        response = self.client.get(reverse('blog:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_posts_list'], [])

    def test_past_post(self):
        """
        Posts with a pub_date in the past are displayed on index page
        """
        create_post('test', days=-30)
        response = self.client.get(reverse('blog:index'))
        self.assertQuerysetEqual(
            response.context['latest_posts_list'],
            ['<Post: test>']
        )

    def test_future_post(self):
        """
        Posts with a pub_date in the future should not be displayed
        """
        create_post('test', days=30)
        response = self.client.get(reverse('blog:index'))
        self.assertQuerysetEqual(
            response.context['latest_posts_list'],
            []
        )

    def test_past_and_future_posts(self):
        """
        Posts exist with pub_dates in the past and future
        but only the posts with a pub_date in the past should
        be displayed
        """
        create_post('past', days=-5)
        create_post('future', days=5)
        response = self.client.get(reverse('blog:index'))
        self.assertQuerysetEqual(
            response.context['latest_posts_list'],
            ['<Post: past>']
        )

    def test_multiple_past_posts(self):
        """
        Index should be able to show multiple posts with
        pub_dates from the past
        """
        create_post('past', days=-5)
        create_post('still past', days=-10)
        create_post('very past', days=-100)
        response = self.client.get(reverse('blog:index'))
        self.assertQuerysetEqual(
            response.context['latest_posts_list'],
            ['<Post: past>', '<Post: still past>', '<Post: very past>']
        )

class PostDetailViewTests(TestCase):
    def test_future_post(self):
        """
        The detail view of a post with a pub_date in the future
        should return a 404 not found
        """
        future_post = create_post('future', days=10)
        url = reverse('blog:detail', args=(future_post.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_post(self):
        """
        The detail view should show a post with a pub_date in the past
        """
        past_post = create_post('past', days=-10)
        url = reverse('blog:detail', args=(past_post.id,))
        response = self.client.get(url)
        self.assertContains(response, past_post.title)
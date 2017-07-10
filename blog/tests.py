import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Post, Tag

def create_post(title, days):
    """
    Create a post with the given title name and published the
    the number of 'days' offset to now (negative for questions published
    in the past, positive for those that have yet to be published)
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Post.objects.create(title=title, body='test', pub_date=time)


def create_tag(tag_name):
    return Tag.objects.create(word=tag_name)



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

    def test_no_tags(self):
        """
        Index view won't show any tags if post doesn't have any
        """
        post = create_post('test', days=-5)
        self.assertQuerysetEqual(post.tags.all(), [])

    def test_show_tag(self):
        """
        Index view should show a tag if it has one
        """
        post = create_post('test', days=-5)
        tag = create_tag('mytag')
        post.tags.add(tag)
        url = reverse('blog:detail', args=(post.id,))
        response = self.client.get(url)
        self.assertContains(response, tag.word)

    def test_show_multiple_tags(self):
        """
        Index view should show multiple tags if post has them
        """
        post = create_post('test', days=-5)
        tag_1 = create_tag('mytag')
        post.tags.add(tag_1)
        tag_2 = create_tag('othertag')
        post.tags.add(tag_2)
        url = reverse('blog:detail', args=(post.id,))
        response = self.client.get(url)
        self.assertQuerysetEqual(
            list(post.tags.all()),
            ['<Tag: mytag>', '<Tag: othertag>'])


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

    def test_no_tags(self):
        """
        Detail view won't show any tags if post doesn't have any
        """
        post = create_post('test', days=-5)
        self.assertQuerysetEqual(post.tags.all(), [])

    def test_show_tag(self):
        """
        Post detail view should show a tag if it has one
        """
        post = create_post('test', days=-5)
        tag = create_tag('mytag')
        post.tags.add(tag)
        url = reverse('blog:detail', args=(post.id,))
        response = self.client.get(url)
        self.assertContains(response, tag.word)

    def test_show_multiple_tags(self):
        """
        Post detail view should show multiple tags if post has them
        """
        post = create_post('test', days=-5)
        tag_1 = create_tag('mytag')
        post.tags.add(tag_1)
        tag_2 = create_tag('othertag')
        post.tags.add(tag_2)
        url = reverse('blog:detail', args=(post.id,))
        response = self.client.get(url)
        self.assertQuerysetEqual(
            list(post.tags.all()),
            ['<Tag: mytag>', '<Tag: othertag>'])


class TagBy_viewViewTests(TestCase):
    def test_posts_for_tag(self):
        """
        Show all the posts that a tag is associated with

        """
        post = create_post('test', days=-8)
        tag = create_tag('testing')
        post.tags.add(tag)
        post_2 = create_post('othertest', days=-10)
        post_2.tags.add(tag)

        get_tag = Tag.objects.filter(word='testing')
        get_post = Post.objects.filter(tags__in=get_tag)

        url = reverse('blog:by_tag', kwargs=({'tag_word': tag.word}))
        response = self.client.get(url)
        # Check to make sure queryset is correct
        self.assertQuerysetEqual(
            list(get_post),
            ['<Post: test>', '<Post: othertest>']
        )
        # Check to make sure posts are actually visible to user
        self.assertContains(response, get_post.first().title)
        self.assertContains(response, get_post.first().body)
        self.assertContains(response, get_post.last().title)
        self.assertContains(response, get_post.last().body)

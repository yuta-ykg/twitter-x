from django.test import TestCase
from django.contrib.auth.models import User
from .models import Post, Follow, Like

class PostTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password')
        self.user2 = User.objects.create_user(username='user2', password='password')

    def test_create_post(self):
        self.client.login(username='user1', password='password')
        response = self.client.post('/', {'content': 'Hello World'})
        self.assertEqual(response.status_code, 302) # Redirect to index
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.first().content, 'Hello World')

    def test_follow_user(self):
        self.client.login(username='user1', password='password')
        response = self.client.get(f'/follow/{self.user2.username}/')
        self.assertTrue(Follow.objects.filter(follower=self.user1, following=self.user2).exists())

        # Unfollow
        response = self.client.get(f'/follow/{self.user2.username}/')
        self.assertFalse(Follow.objects.filter(follower=self.user1, following=self.user2).exists())

    def test_like_post(self):
        post = Post.objects.create(user=self.user2, content='User2 Post')
        self.client.login(username='user1', password='password')

        # Like
        response = self.client.get(f'/like/{post.id}/')
        self.assertTrue(Like.objects.filter(user=self.user1, post=post).exists())

        # Unlike
        response = self.client.get(f'/like/{post.id}/')
        self.assertFalse(Like.objects.filter(user=self.user1, post=post).exists())

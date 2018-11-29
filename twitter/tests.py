import json
import random
import string
from django.contrib.auth.models import User
from twitter.tweets.models import Tweet
from rest_framework.test import APITestCase
from faker import Faker
fake = Faker()


class TwitterAPITestCase(APITestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.users_count = random.randint(2, 50)
        self.tweets_count = random.randint(2, 100)
        self.admin = self.random_user()
        self.users = []
        self.tweets = []

    def setUp(self):
        # Populate users
        self.users.append(User.objects.create_superuser(**self.admin))
        for i in range(1, self.users_count):
            self.users.append(User.objects.create_user(**self.random_user()))
        self.assertEqual(len(self.users), self.users_count)

        # Populate tweets
        for i in range(0, self.tweets_count):
            self.tweets.append(Tweet.objects.create(user_id=random.choice(self.users).pk, text=fake.text()))
        self.assertEqual(len(self.tweets), self.tweets_count)

        # Authenticate all requests
        self.authenticate()

    def tearDown(self):
        # Cleanup tweets
        for t in self.tweets:
            t.delete()
        self.tweets = []
        self.assertEqual(len(self.tweets), 0)

        # Cleanup users
        for u in self.users:
            u.delete()
        self.users = []
        self.assertEqual(len(self.users), 0)

    def authenticate(self):
        response = self.client.post('/api/token', {'username': self.admin['username'], 'password': self.admin['password']})
        content = json.loads(response.content)
        self.assertIn('access', content)
        self.assertIn('refresh', content)
        self.token_access = content.get('access')
        self.token_refresh = content.get('refresh')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_access)

    def random_user(self):
        return {
            'username': fake.user_name(),
            'email': fake.email(),
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'password': fake.password()
        }

    def random_tweet(self):
        return {
            'user': random.choice(self.users).pk,
            'text': fake.text(140) 
        }

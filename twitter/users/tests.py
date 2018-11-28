import json
import random
from django.contrib.auth.models import User
from django.urls import reverse
from twitter.tests import TwitterAPITestCase
from faker import Faker
fake = Faker()


class TwitterAPIUserTestCase(TwitterAPITestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_user_get_list(self):
        response = self.client.get('/api/users')
        self.assertEqual(200, response.status_code)
        count = json.loads(response.content).get('count')
        self.assertEqual(count, self.users_count)

    def test_user_get_detail(self):
        user = random.choice(self.users)
        response = self.client.get(f'/api/users/{user.pk}')
        self.assertEqual(200, response.status_code)

        username = json.loads(response.content).get('username')
        email = json.loads(response.content).get('email')
        self.assertEqual(username, user.username)
        self.assertEqual(email, user.email)

    def test_user_post(self):
        response = self.client.post('/api/users', self.random_user())
        self.assertEqual(201, response.status_code)

    def test_user_delete(self):
        user = random.choice(self.users)
        response = self.client.delete(f'/api/users/{user.pk}')
        self.assertEqual(204, response.status_code)

    def test_user_put_invalid(self):
        user = random.choice(self.users)
        response = self.client.put(f'/api/users/{user.pk}', {'username': fake.user_name()})
        self.assertNotEqual(200, response.status_code)

    def test_user_put_valid(self):
        user = random.choice(self.users)
        new_user = self.random_user()
        response = self.client.put(f'/api/users/{user.pk}', new_user)
        content = json.loads(response.content)
        self.assertEqual(200, response.status_code)
        self.assertEqual(content.get('username'), new_user['username'])
        self.assertEqual(content.get('email'), new_user['email'])
        self.assertEqual(content.get('first_name'), new_user['first_name'])
        self.assertEqual(content.get('last_name'), new_user['last_name'])

    def test_user_patch(self):
        user = random.choice(self.users)
        response = self.client.patch(f'/api/users/{user.pk}', {'username': fake.user_name()})
        self.assertEqual(200, response.status_code)

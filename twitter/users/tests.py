import json
import random
from django.contrib.auth.models import User
from django.urls import reverse
from twitter.tests import TwitterTestCase


class UserAPIViewTestCase(TwitterTestCase):
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
        data = {
            'username': 'laura',
            'email': 'laura.bakotic@fer.hr',
            'password': 'demo1234'
        }
        response = self.client.post('/api/users', data)
        self.assertEqual(201, response.status_code)

    def test_user_delete(self):
        data = {
            'username': 'laura',
            'email': 'laura.bakotic@fer.hr',
            'password': 'demo1234'
        }
        user = User.objects.create_user(**data)
        response = self.client.delete(f'/api/users/{user.pk}')
        self.assertEqual(204, response.status_code)

import json
import random
from django.contrib.auth.models import User
from django.urls import reverse
from twitter.tests import TwitterTestCase


class UserAPIViewTestCase(TwitterTestCase):
    def setUp(self):
        super(UserAPIViewTestCase, self).setUp()

        self.users = []
        self.n = random.randint(2, 10)
        for i in range(1, self.n):
            self.users.append(User.objects.create_user(self.random_string(), self.random_string(), self.random_string()))

    def tearDown(self):
        for u in self.users:
            u.delete()
        self.users = []

        super(UserAPIViewTestCase, self).tearDown()

    def test_user_get_list(self):
        response = self.client.get('/api/users')
        self.assertEqual(200, response.status_code)
        n = len(json.loads(response.content).get('results'))
        self.assertEqual(n, self.n)

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

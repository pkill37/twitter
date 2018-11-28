import json
from django.contrib.auth.models import User
from rest_framework.test import APITestCase


class TwitterTestCase(APITestCase):
    def setUp(self):
        self.username = 'john'
        self.email = 'john.doe@fer.hr'
        self.password = 'demo1234'
        self.user = User.objects.create_superuser(self.username, self.email, self.password)
        self.authenticate()

    def tearDown(self):
        self.user.delete()

    def authenticate(self):
        response = self.client.post('/api/token', {'username': self.username, 'password': self.password})
        response = json.loads(response.content)
        self.assertIn('access', response)
        self.assertIn('refresh', response)
        self.token = response.get('access')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def random_string(self):
        import uuid
        return uuid.uuid4().hex.upper()[0:6]

import json
import random
from twitter.tests import TwitterAPITestCase
from faker import Faker
fake = Faker()


class TwitterAPITokenTestCase(TwitterAPITestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_token(self):
        response = self.client.post(f'/api/token', {'username': self.admin['username'], 'password': self.admin['password']})
        self.assertEqual(200, response.status_code)
        content = json.loads(response.content)
        self.assertIn('access', content)
        self.assertIn('refresh', content)

    def test_token_refresh(self):
        response = self.client.post(f'/api/token/refresh', {'refresh': self.token_refresh})
        self.assertEqual(200, response.status_code)
        content = json.loads(response.content)
        self.assertIn('access', content)

    def test_token_verify(self):
        response = self.client.post(f'/api/token/verify', {'token': self.token_access})
        self.assertEqual(200, response.status_code)
        content = json.loads(response.content)
        self.assertEqual({}, content)


class TwitterAPIUserTweetsTestCase(TwitterAPITestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_user_tweets_get_list(self):
        user = random.choice(self.users)
        response = self.client.get(f'/api/users/{user.pk}/tweets')
        self.assertEqual(200, response.status_code)

    def test_user_tweets_post(self):
        user = random.choice(self.users)
        response = self.client.post(f'/api/users/{user.pk}/tweets', {'user': user.pk, 'text': fake.text(140)})
        self.assertEqual(201, response.status_code)

    def test_user_tweets_get_detail(self):
        tweet = random.choice(self.tweets)
        response = self.client.get(f'/api/users/{tweet.user.pk}/tweets/{tweet.pk}')
        self.assertEqual(200, response.status_code)

    def test_user_tweets_delete(self):
        tweet = random.choice(self.tweets)
        response = self.client.delete(f'/api/users/{tweet.user.pk}/tweets/{tweet.pk}')
        self.assertEqual(204, response.status_code)

    def test_user_tweets_put_invalid(self):
        tweet = random.choice(self.tweets)
        response = self.client.put(f'/api/users/{tweet.user.pk}/tweets/{tweet.pk}', {'text': fake.text(140)})
        self.assertNotEqual(200, response.status_code)

    def test_user_tweets_put_valid(self):
        tweet = random.choice(self.tweets)
        response = self.client.put(f'/api/users/{tweet.user.pk}/tweets/{tweet.pk}', {'user': tweet.user.pk, 'text': fake.text(140)})
        self.assertEqual(200, response.status_code)

    def test_user_tweets_patch(self):
        tweet = random.choice(self.tweets)
        response = self.client.patch(f'/api/users/{tweet.user.pk}/tweets/{tweet.pk}', {'text': fake.text(140)})
        self.assertEqual(200, response.status_code)


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

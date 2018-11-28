import json
import random
from twitter.tweets.models import Tweet
from twitter.tests import TwitterAPITestCase
from faker import Faker
fake = Faker()


class TwitterAPITweetTestCase(TwitterAPITestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_tweet_get_list(self):
        response = self.client.get('/api/tweets')
        self.assertEqual(200, response.status_code)
        count = json.loads(response.content).get('count')
        self.assertEqual(count, self.tweets_count)

    def test_tweet_get_detail(self):
        tweet = random.choice(self.tweets)
        response = self.client.get(f'/api/tweets/{tweet.pk}')
        self.assertEqual(200, response.status_code)

        user = json.loads(response.content).get('user')
        text = json.loads(response.content).get('text')
        self.assertEqual(user, tweet.user.pk)
        self.assertEqual(text, tweet.text)

    def test_tweet_post(self):
        response = self.client.post('/api/tweets', self.random_tweet())
        self.assertEqual(201, response.status_code)

    def test_tweet_delete(self):
        tweet = random.choice(self.tweets)
        response = self.client.delete(f'/api/tweets/{tweet.pk}')
        self.assertEqual(204, response.status_code)

    def test_tweet_put_invalid(self):
        tweet = random.choice(self.tweets)
        response = self.client.put(f'/api/tweets/{tweet.pk}', {'text': fake.text(140)})
        self.assertNotEqual(200, response.status_code)

    def test_tweet_put_valid(self):
        tweet = random.choice(self.tweets)
        new_tweet = self.random_tweet()
        response = self.client.put(f'/api/tweets/{tweet.pk}', new_tweet)
        content = json.loads(response.content)
        self.assertEqual(200, response.status_code)
        self.assertEqual(content.get('user'), new_tweet['user'])
        self.assertEqual(content.get('text'), new_tweet['text'])

    def test_tweet_patch(self):
        tweet = random.choice(self.tweets)
        response = self.client.patch(f'/api/tweets/{tweet.pk}', {'text': fake.text(140)})
        self.assertEqual(200, response.status_code)

from twitter.tweets.models import Tweet
from rest_framework import serializers


class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = ('id', 'user', 'text',)

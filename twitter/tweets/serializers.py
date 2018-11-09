from twitter.tweets.models import Tweet
from rest_framework import serializers


class TweetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tweet
        fields = ('text',)

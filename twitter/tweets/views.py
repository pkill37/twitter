from rest_framework import viewsets
from twitter.tweets.models import Tweet
from twitter.tweets.serializers import TweetSerializer


class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all().order_by('-created_at')
    serializer_class = TweetSerializer

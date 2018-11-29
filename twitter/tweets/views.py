from rest_framework import viewsets
from twitter.tweets.models import Tweet
from twitter.tweets.serializers import TweetSerializer


class TweetViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows tweets to be viewed or edited.
    """
    queryset = Tweet.objects.all().order_by('-created_at')
    serializer_class = TweetSerializer
    ordering_fields = ('text',)

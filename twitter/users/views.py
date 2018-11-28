from django.contrib.auth.models import User
from rest_framework import viewsets
from twitter.users.serializers import UserSerializer
from twitter.tweets.models import Tweet
from twitter.tweets.serializers import TweetSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class UserTweetsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows the tweets of users to be viewed or edited.
    """
    serializer_class = TweetSerializer

    def get_queryset(self):
        return Tweet.objects.filter(user=self.kwargs['user_pk'])

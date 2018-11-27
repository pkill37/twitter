from django.db import models
from twitter.models import TimestampableModel
from django.contrib.auth.models import User


class Tweet(TimestampableModel):
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    text = models.CharField(max_length=140)

from django.db import models
from twitter.models import TimestampableModel
from django.contrib.auth.models import User


class Tweet(TimestampableModel):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=140)

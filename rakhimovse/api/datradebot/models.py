from django.db import models


class User(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    wallet = models.FloatField(default=0)
    invited_by = models.ForeignKey('self', models.SET_NULL, null=True, blank=True)
    registered = models.DateTimeField(auto_now_add=True)


class Subscription(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    valid_until = models.DateTimeField()

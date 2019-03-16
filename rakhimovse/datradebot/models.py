from dateutil.relativedelta import relativedelta
from django.db import models, transaction
from django.utils import timezone
import random
import string


def get_promo():
    symbols = string.digits + string.ascii_uppercase
    return ''.join([random.choice(symbols) for i in range(Promo.PROMO_LENGTH)])


class User(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    wallet = models.FloatField(default=0)
    invited_by = models.ForeignKey('self', models.SET_NULL, null=True, blank=True)
    registered = models.DateTimeField(auto_now_add=True)

    @property
    def subscription_active_until(self):
        subscriptions = self.subscription_set.all()
        return subscriptions.aggregate(models.Max('active_until'))['active_until__max']

    @property
    def is_subscription_active(self):
        return timezone.now() <= self.subscription_active_until()


class Subscription(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    active_until = models.DateTimeField()


class Promo(models.Model):
    DAY7 = 'day7'
    MONTH1 = 'month1'
    MONTH3 = 'month3'
    MONTH6 = 'month6'
    MONTH12 = 'month12'
    PERIOD_CHOICES = (
        (DAY7, '7 days'),
        (MONTH1, '1 month'),
        (MONTH3, '3 months'),
        (MONTH6, '6 months'),
        (MONTH12, '12 months'),
    )
    PROMO_LENGTH = 8

    id = models.CharField(primary_key=True, max_length=PROMO_LENGTH, default=get_promo)
    period = models.CharField(max_length=15, choices=PERIOD_CHOICES, default=DAY7)
    subscription = models.OneToOneField(Subscription, models.CASCADE, null=True)
    active_until = models.DateTimeField(default=timezone.datetime.max)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def is_active(self):
        return timezone.now() <= self.active_until

    def issue(self, user):
        # TODO Что делать, если уже имеется активная подписка?
        if self.period == Promo.DAY7:
            delta = relativedelta(days=7)
        elif self.period == Promo.MONTH1:
            delta = relativedelta(months=1)
        elif self.period == Promo.MONTH3:
            delta = relativedelta(months=3)
        elif self.period == Promo.MONTH6:
            delta = relativedelta(months=6)
        elif self.period == Promo.MONTH12:
            delta = relativedelta(months=12)
        else:
            raise ValueError
        active_until = timezone.now() + delta

        with transaction.atomic():
            self.subscription = Subscription.objects.create(user=user, active_until=active_until)
            self.save()

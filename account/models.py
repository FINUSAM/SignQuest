from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserStatsModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    learning_counter = models.IntegerField(default=7)
    a = models.FloatField(default=1)
    aa = models.FloatField(default=1)
    i = models.FloatField(default=1)
    ii = models.FloatField(default=1)
    u = models.FloatField(default=1)
    uu = models.FloatField(default=1)
    r = models.FloatField(default=1)
    e = models.FloatField(default=0)
    ee = models.FloatField(default=0)
    ai = models.FloatField(default=0)
    o = models.FloatField(default=0)
    oo = models.FloatField(default=0)
    au = models.FloatField(default=0)
    am = models.FloatField(default=0)
    ah = models.FloatField(default=0)

    def __str__(self):
        return f"{self.user.username}"
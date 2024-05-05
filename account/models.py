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
    flashcard_allowed_levels = models.IntegerField(default=1)
    flashcard_1 = models.IntegerField(default=0)
    flashcard_2 = models.IntegerField(default=0)
    flashcard_3 = models.IntegerField(default=0)
    flashcard_4 = models.IntegerField(default=0)
    flashcard_5 = models.IntegerField(default=0)
    flashcard_6 = models.IntegerField(default=0)
    flashcard_7 = models.IntegerField(default=0)
    ordering_alphabet = models.IntegerField(default=0)
    ordering_image = models.IntegerField(default=0)
    quiz_1 = models.IntegerField(default=0)
    quiz_2 = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}"
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class GroupModel(models.Model):
    group_name = models.CharField(max_length=100)

    def __str__(self):
        return self.group_name

class MessageModel(models.Model):
    message = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # Change on_delete behavior
    group = models.ForeignKey(GroupModel, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.message
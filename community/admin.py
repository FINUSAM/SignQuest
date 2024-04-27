from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.GroupModel)
admin.site.register(models.MessageModel)
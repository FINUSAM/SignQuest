from django.db import models

# Create your models here.

class MalayalamAlphabetModel(models.Model):
    eng = models.CharField(max_length=4)
    mal = models.CharField(max_length=3)
    image = models.ImageField(upload_to='uploads/')

    def __str__(self) -> str:
        return self.eng

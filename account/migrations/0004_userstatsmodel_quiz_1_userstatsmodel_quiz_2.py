# Generated by Django 5.0.4 on 2024-05-05 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_userstatsmodel_ordering_alphabet_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userstatsmodel',
            name='quiz_1',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userstatsmodel',
            name='quiz_2',
            field=models.IntegerField(default=0),
        ),
    ]

# Generated by Django 3.0.4 on 2020-11-10 03:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20201108_1434'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pagetext',
            options={'ordering': ['-created_on']},
        ),
        migrations.AddField(
            model_name='pageurl',
            name='title',
            field=models.CharField(default='', max_length=500),
        ),
    ]

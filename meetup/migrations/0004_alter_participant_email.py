# Generated by Django 5.0.6 on 2024-06-18 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetup', '0003_alter_myuser_image_speaker_meetup'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
    ]

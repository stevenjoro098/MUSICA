# Generated by Django 3.2.5 on 2022-01-24 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Music', '0007_alter_song_song_length'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='audio_file',
            field=models.FileField(default=1, upload_to='Media/Audio'),
            preserve_default=False,
        ),
    ]

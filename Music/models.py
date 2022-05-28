from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User


class Album(models.Model):
    artist = models.ForeignKey(User, related_name='user_albums', on_delete=models.CASCADE)
    album_name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    album_image = models.ImageField('Media/Music/Albums')
    uploaded = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='users_likes', blank=True)
    class Meta:
        ordering = ['-uploaded']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.album_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.album_name

    def total_likes(self):
        return self.likes.count()


class Song(models.Model):
    artist = models.ForeignKey(User, related_name='users_songs', on_delete=models.CASCADE)
    song_name = models.CharField(max_length=200)
    album = models.ForeignKey(Album, related_name='album_songs', on_delete=models.CASCADE, blank=True, default=1)
    image = models.ImageField(upload_to='Media/Music/Songs')
    uploaded = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)
    song_length = models.TimeField(default='1:20:20')
    audio_file = models.FileField(upload_to='Media/Audio')
    audience = models.ManyToManyField(User, related_name='user_collections', blank=True)
    likes = models.ManyToManyField(User, related_name='user_likes', blank=True)

    class Meta:
        ordering = ['-uploaded']

    def total_likes(self):
        return self.likes.count()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.song_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.song_name


class EmailsApproval(models.Model):
    email = models.EmailField()

    def __str__(self):
        return self.email
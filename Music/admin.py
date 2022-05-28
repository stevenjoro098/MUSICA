from django.contrib import admin
from .models import Album, Song, EmailsApproval


# Register your models here.

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ['album_name', 'uploaded']


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ['artist', 'song_name', 'album', 'uploaded']
    prepopulated_fields = {'slug': ('song_name',)}


@admin.register(EmailsApproval)
class EmailApprovalAdmin(admin.ModelAdmin):
    list_display = ['email']

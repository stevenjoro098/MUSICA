from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Song, Album, EmailsApproval


class EmailForm(forms.ModelForm):
    #email = forms.EmailField()
    class Meta:
        model = EmailsApproval
        fields = ['email']


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


class MusicUploadForm(forms.Form):
    song_name = forms.CharField()
    album = forms.ModelChoiceField(queryset=Album.objects.all())

    class Meta:
        model = Song
        fields = ('song_name', 'album')

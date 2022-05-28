from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, FormView
from .models import Song, Album
from .forms import RegistrationForm, EmailForm
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin


# Create your views here.

class MusicListView(ListView):
    model = Song
    paginate_by = 4
    template_name = 'music/music_list.html'
    context_object_name = 'songs'

    def post(self, request, *args, **kwargs):
        user = User.objects.get(username=self.request.user)
        song = get_object_or_404(Song, slug=self.request.POST['slug'])
        if song:
            song.audience.add(user)  # many-to-many relationship
            messages.success(request, "Added Successful")
        return HttpResponseRedirect(reverse_lazy('list_music'))


class MusicView(ListView):
    """ Home page list of last 6 songs uploaded.."""
    model = Song
    template_name = 'music/home.html'
    context_object_name = 'songs'

    def get_queryset(self):
        """Return the Last 6 songs added..."""
        return Song.objects.all()[:6]

    def get_context_data(self, *args,**kwargs):
        context = super(MusicView, self).get_context_data(**kwargs)
        context['email_form'] = EmailForm
        context['albums'] = Album.objects.all()[:3]
        return context


class MusicCollectionListView(ListView):
    """ Music added by user as collection"""
    model = Song
    template_name = 'music/music_collection.html'
    context_object_name = 'music_collection'

    def get_queryset(self):
        return Song.objects.filter(audience__in=[self.request.user])


class MusicDetailView(DetailView):
    model = Song
    template_name = 'music/music_detail.html'

    def post(self, request, *args, **kwargs):
        song = get_object_or_404(Song, id=request.POST['like'])
        if song:
            song.likes.add(self.request.user)
            return redirect('music_details', song.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['song_likes'] = self.get_object().total_likes()
        return context

def Registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy('login'))
    else:
        form = RegistrationForm()
    return render(request, 'registration/registration.html', {'form': form})


class AlbumView(CreateView):
    """Create New Album Instance"""
    model = Album
    fields = ['album_name', 'album_image']
    template_name = 'album/create_album.html'
    success_url = reverse_lazy('list_artist_album')

    def form_valid(self, form):
        form.instance.artist = self.request.user  # override form method for artist value
        return super(AlbumView, self).form_valid(form)


class AlbumListView(ListView):
    model = Album
    context_object_name = 'albums'
    template_name = 'album/list_albums.html'

    def get_queryset(self):
        """Override queryset to fetch only albums created by artist/user"""
        qs = super().get_queryset()
        return qs.filter(artist=self.request.user)  # django lookup


class UploadSongView(CreateView):
    model = Song
    fields = ['song_name', 'album', 'image', 'audio_file']
    template_name = 'music/upload.html'
    success_url = reverse_lazy('home')

    def get_initial(self):
        """Provide initial data to Form. i.e Fetch only albums created by Artist/User"""
        initial = super(UploadSongView, self).get_initial()
        album = Album.objects.filter(artist=self.request.user)
        print(album)
        initial['album'] = album
        return initial

    def form_valid(self, form):
        form.instance.artist = self.request.user
        return super(UploadSongView, self).form_valid(form)


class EmailApprovalView(SuccessMessageMixin, FormView):
    template_name = None
    form_class = EmailForm
    success_url = reverse_lazy('home')
    success_message = "Email Sent Successfully"

    def form_valid(self, form):
        print(form.cleaned_data)
        form.save()  # add user email to db for approvals.
        return super().form_valid(form)


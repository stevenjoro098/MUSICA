from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import MusicView, MusicDetailView,EmailApprovalView, Registration, UploadSongView, AlbumView, AlbumListView, MusicListView, MusicCollectionListView
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', MusicView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', Registration, name='register'),
    path('upload/', UploadSongView.as_view(), name='upload'),
    path('album/upload/', AlbumView.as_view(), name='upload_album'),
    path('music/list/', MusicListView.as_view(), name='list_music'),
    path('music/collection/', MusicCollectionListView.as_view(), name='music_collection'),
    path('music/detail/<int:pk>', MusicDetailView.as_view(), name='music_details'),
    path('emails/approval/', EmailApprovalView.as_view(), name='approval'),
    path('list/albums/', AlbumListView.as_view(), name='list_artist_album'),

]
urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)

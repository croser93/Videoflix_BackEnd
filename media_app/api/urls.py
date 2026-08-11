from django.urls import path
from .views import VideoView, HlsIndexView, HlsSegmentView



urlpatterns = [
    path('video/', VideoView.as_view(), name='video'),
    path('video/<int:movie_id>/<str:resolution>/index.m3u8', HlsIndexView.as_view(), name='hls_index'),
    path('video/<int:movie_id>/<str:resolution>/<str:segment>/', HlsSegmentView.as_view(), name='hls_segment'),
]

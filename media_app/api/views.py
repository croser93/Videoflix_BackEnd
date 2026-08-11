
from rest_framework.views import APIView
from media_app.models import VideoModel
from rest_framework.response import Response
from .serializer import VideoSerializer
from rest_framework.permissions import  IsAuthenticated
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django.conf import settings
from pathlib import Path



class VideoView(APIView):
    """
    List all available videos.

    Endpoints:
    - GET    /api/video/ - Retrieve a list of all videos
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        videos = VideoModel.objects.all()
        serializer = VideoSerializer(videos, many=True, context={'request': request})
        return Response(serializer.data, status=200)

class HlsIndexView(APIView):
    """
    Serve the HLS master playlist for a video at a given resolution.

    Endpoints:
    - GET    /api/video/{movie_id}/{resolution}/index.m3u8 - Retrieve the HLS playlist file
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, movie_id, resolution):

        hls_index = get_object_or_404(VideoModel,pk=movie_id)
        path = Path(settings.MEDIA_ROOT) /  'videos' / str(movie_id)  /str(resolution) / "index.m3u8"
        if path.exists():
            return FileResponse(open(path, 'rb'),content_type='application/vnd.apple.mpegurl')
        else:
            return Response(status=404)

class HlsSegmentView(APIView):
    """
    Serve a single HLS video segment for a video at a given resolution.

    Endpoints:
    - GET    /api/video/{movie_id}/{resolution}/{segment}/ - Retrieve a binary HLS segment file
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, movie_id, resolution, segment):

        hls_index = get_object_or_404(VideoModel,pk=movie_id)
        path = Path(settings.MEDIA_ROOT) /  'videos' / str(movie_id)  /str(resolution) / str(segment)
        if path.exists():
            return FileResponse(open(path, 'rb'),content_type='video/MP2T')
        else:
            return Response(status=404)


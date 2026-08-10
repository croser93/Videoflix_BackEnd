
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

    permission_classes = [IsAuthenticated]

    def get(self, request):
        videos = VideoModel.objects.all()
        serializer = VideoSerializer(videos, many=True, context={'request': request})
        return Response(serializer.data, status=200)

class HlsIndexView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, movie_id, resolution):

        hls_index = get_object_or_404(VideoModel,pk=movie_id)
        path = Path(settings.MEDIA_ROOT) /  'videos' / str(movie_id)  /str(resolution) / "index.m3u8"
        if path.exists():
            return FileResponse(open(path, 'rb'),content_type='application/vnd.apple.mpegurl')
        else:
            return Response(status=404)


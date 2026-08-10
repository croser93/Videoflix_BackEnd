
from rest_framework.views import APIView
from media_app.models import VideoModel
from rest_framework.response import Response
from .serializer import VideoSerializer



class VideoView(APIView):

    def get(self, request):
        videos = VideoModel.objects.all()
        serializer = VideoSerializer(videos, many=True, context={'request': request})
        print(serializer.data)
        return Response(serializer.data, status=200)

from rest_framework.views import APIView
from media_app.models import VideoModel
from rest_framework.response import Response
from .serializer import VideoSerializer
from rest_framework.permissions import  IsAuthenticated



class VideoView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        videos = VideoModel.objects.all()
        serializer = VideoSerializer(videos, many=True, context={'request': request})
        return Response(serializer.data, status=200)
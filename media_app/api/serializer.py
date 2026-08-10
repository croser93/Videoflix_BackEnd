from rest_framework import serializers
from media_app.models import VideoModel
from django.contrib.auth import authenticate


class VideoSerializer(serializers.ModelSerializer):

    class Meta:
        model = VideoModel 
        fields = ['id','title','video_file', 'thumbnail_url', 'category', 'created_at' ]


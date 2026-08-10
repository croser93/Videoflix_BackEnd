from rest_framework import serializers
from media_app.models import VideoModel
from django.contrib.auth import authenticate


class VideoSerializer(serializers.ModelSerializer):

    class Meta:
        model = VideoModel 
        fields = ['id','title','description', 'thumbnail_url', 'category', 'created_at' ]


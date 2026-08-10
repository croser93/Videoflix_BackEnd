from rest_framework.test import APITestCase
from auth_app.models import CustomUser
from media_app.models import VideoModel
from django.urls import reverse
from rest_framework import status
from django.db.models.signals import post_save
from media_app.signals import video_post_Save

class VideoTest(APITestCase):

    def setUp(self):

        post_save.disconnect(video_post_Save, sender=VideoModel)
        self.video = VideoModel.objects.create(title='Movie Title', description="Movie Description", video_file="videos/test.mp4", thumbnail_url="thumbnails/test.jpg", category="Drama")    
        self.user = CustomUser.objects.create_user(email='test@gmx.de', password='123456')
        self.user.is_active = True
        self.user.save()

    def test_get_video(self):
        url = reverse('video')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data[0]['id'], self.video)
        self.assertEqual(response.data[0]['created_at'], self.video.created_at.isoformat().replace('+00:00', 'Z'))
        self.assertEqual(response.data[0]['title'], self.video.title)
        self.assertEqual(response.data[0]['description'], self.video.description)
        self.assertTrue(response.data[0]['thumbnail_url'])
        self.assertEqual(response.data[0]['category'], self.video.category)
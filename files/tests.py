from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UploadedFile
import json
import os
from django.conf import settings

class SignupViewTest(APITestCase):
    def test_signup(self):
        url = reverse('signup')  # assuming you have a URL route named 'signup'
        data = {
            'username': 'testuser',
            'password': 'testpassword',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='testuser').exists())

class FileUploadTest(APITestCase):
    def setUp(self):
        # Create user and obtain token
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

    def tearDown(self):
        # Clean up the uploaded file after each test
        file_path = os.path.join(settings.UPLOADS_FOLDER, 'test.txt')
        if os.path.exists(file_path):
            os.remove(file_path)


    def test_file_upload(self):
        url = reverse('file-upload')  
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        file = SimpleUploadedFile('test.txt', b'This is a test file.', content_type='text/plain')
        response = self.client.post(url, {'file': file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class FileUpdateByIdTest(APITestCase):
    def setUp(self):
        # Create user and obtain token
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        url_upload_file = reverse('file-upload')
        file = SimpleUploadedFile('test.txt', b'This is a test file.', content_type='text/plain')
        self.client.post(url_upload_file, {'file': file}, format='multipart')
        self.file = UploadedFile.objects.get(name='test.txt')

    def tearDown(self):
        # Clean up the uploaded file after each test
        file_path = os.path.join(settings.UPLOADS_FOLDER, 'updatedfile.txt')
        if os.path.exists(file_path):
            os.remove(file_path)    


    def test_file_update(self):
        pk = self.file.id 
        url = reverse('file-rename', kwargs={'pk': pk})

        updated_data = {"name": "updatedfile.txt"}

        response = self.client.put(url, json.dumps(updated_data), content_type='application/json')

        self.assertEqual(response.status_code, 200)

        self.file.refresh_from_db()
        self.assertEqual(self.file.name, 'updatedfile.txt') 


class FileDownloadTest(APITestCase):
    def setUp(self):
        # Create user and obtain token
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.file_content = b'This is a test file.'
        self.uploaded_filename = 'test.txt'

        url_upload_file = reverse('file-upload')
        file = SimpleUploadedFile(self.uploaded_filename, self.file_content, content_type='text/plain')
        self.client.post(url_upload_file, {'file': file}, format='multipart')
        self.file = UploadedFile.objects.get(name=self.uploaded_filename)


    def tearDown(self):
        # Clean up the uploaded file after each test
        file_path = os.path.join(settings.UPLOADS_FOLDER, self.uploaded_filename)
        if os.path.exists(file_path):
            os.remove(file_path)

    def test_file_download(self):
        pk = self.file.id 
        url = reverse('file-download', kwargs={'pk': pk})

        response = self.client.get(url, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, self.file_content)

        
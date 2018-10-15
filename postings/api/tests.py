from rest_framework.test import APITestCase
from rest_framework.reverse import reverse as api_reverse
from rest_framework import status

from django.contrib.auth import get_user_model

from postings.models import Blog

User = get_user_model()

class BlogAPITestCase(APITestCase):
	def setUp(self):
		user = User.objects.create(username='testcase', email='testcase@django.com')
		user.set_password('thisistestpass')
		user.save()
		blog_post = Blog.objects.create(
			user=user,
			title='Test Title',
			content='Test Content'
		)

	def test_single_user(self):
		user_count = User.objects.count()
		self.assertEqual(user_count, 1)

	def test_single_blog(self):
		blog_count = Blog.objects.count()
		self.assertEqual(blog_count, 1)

	def test_get_list(self):
		data = {}
		url = api_reverse('api-postings:blog-list-create')
		response = self.client.get(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		print(response.data)

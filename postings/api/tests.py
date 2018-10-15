from rest_framework.test import APITestCase

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

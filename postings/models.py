from django.db import models
from django.urls import reverse
from django.conf import settings

from rest_framework.reverse import reverse as api_reverse

class Blog(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	title = models.CharField(max_length=120, null=True, blank=True)
	content = models.TextField(max_length=120, null=True, blank=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.user.username)

	@property
	def owner(self):
		return self.user

	# get_absolute_url method for api
	def get_api_url(self, request=None):
		return api_reverse(
			'api-postings:blog-rud',
			kwargs={'pk': self.pk},
			request=request
		)

	# use django reverse for its urls
	# def get_absolute_url(self):
	# 	return reverse('')

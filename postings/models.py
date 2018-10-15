from django.db import models

from django.conf import settings

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

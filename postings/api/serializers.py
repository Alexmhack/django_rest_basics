from rest_framework import serializers

from postings.models import Blog

class BlogSerializer(serializers.ModelSerializer):
	class Meta:
		model = Blog
		fields = ('pk', 'user', 'title', 'content', 'timestamp')

		# serializer converts to json and validates the data

from rest_framework import serializers

from postings.models import Blog

class BlogSerializer(serializers.ModelSerializer):
	class Meta:
		model = Blog
		fields = ('pk', 'user', 'title', 'content', 'timestamp')
		read_only_fields = ('user',)

		# serializer converts to json and validates the data
		
	# validate_<field_name>
	def validate_title(self, value):
		qs = Blog.objects.filter(title__iexact=value)

		# excludes the instance
		if self.instance:
			qs = qs.exclude(pk=self.instance.pk)
		if qs.exists():
			raise serializers.ValidationError("This title has already been used")
		return value

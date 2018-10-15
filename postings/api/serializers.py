from rest_framework import serializers

from postings.models import Blog

class BlogSerializer(serializers.ModelSerializer):
	url = serializers.SerializerMethodField(read_only=True)
	
	class Meta:
		model = Blog
		fields = ('url', 'id', 'user', 'title', 'content', 'timestamp')
		read_only_fields = ('user', 'id')

		# serializer converts to json and validates the data
	
	# get_<field_name> method
	def get_url(self, obj):
		request = self.context.get('request')
		return obj.get_api_url(request=request)
		
	# validate_<field_name>
	def validate_title(self, value):
		qs = Blog.objects.filter(title__iexact=value)

		# excludes the instance
		if self.instance:
			qs = qs.exclude(pk=self.instance.pk)
		if qs.exists():
			raise serializers.ValidationError("This title has already been used")
		return value

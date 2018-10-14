from rest_framework import generics

from postings.models import Blog
from .serializers import BlogSerializer

class BlogRUDView(generics.RetrieveUpdateDestroyAPIView):
	lookup_field = "pk"
	queryset = Blog.objects.all().order_by('-timestamp')
	serializer_class = BlogSerializer

	# def get_queryset(self):
	# 	return Blog.objects.all()

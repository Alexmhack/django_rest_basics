from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from postings.models import Blog
from .serializers import BlogSerializer

class BlogRUDView(generics.RetrieveUpdateDestroyAPIView):
	# field which is looked by serializer while rendering json
	# lookup_field = "pk"	"pk" is the default lookup field in generic view
	queryset = Blog.objects.all().order_by('-timestamp')
	serializer_class = BlogSerializer
	permission_classes = (IsAuthenticated,)

	# def get_queryset(self):
	# 	return Blog.objects.all()

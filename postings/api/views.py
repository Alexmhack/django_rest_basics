from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from postings.models import Blog
from .serializers import BlogSerializer

class BlogRUDView(generics.RetrieveUpdateDestroyAPIView):
	# RetrieveUpdateDestroyAPIView / RetrieveAPIView
	# field which is looked by serializer while rendering json
	# lookup_field = "pk"	"pk" is the default lookup field in generic view
	queryset = Blog.objects.all().order_by('-timestamp')
	serializer_class = BlogSerializer
	permission_classes = (IsAuthenticated,)

	# def get_queryset(self):
	# 	return Blog.objects.all()


# class BlogCreateAPIView(generics.CreateAPIView):
# 	serializer_class = BlogSerializer

# 	def get_queryset(self):
# 		return Blog.objects.all()

# 	def perform_create(self, serializer):
# 		serializer.save(user=self.request.user)


# view that supports both GET and POST method
class BlogListAPIView(mixins.CreateModelMixin, generics.ListAPIView):
	serializer_class = BlogSerializer

	def get_queryset(self):
		return Blog.objects.all().order_by('-timestamp')

	# add create as well as list functionality to view
	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

	# adds the post method in allowed methods list
	def post(self, request, *args, **kwargs):
		return self.create(request, *args, **kwargs)

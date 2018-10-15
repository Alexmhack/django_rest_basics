from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from django.db.models import Q

from postings.models import Blog
from .serializers import BlogSerializer
from .permissions import IsOwnerOrReadOnly

class BlogRUDView(generics.RetrieveUpdateDestroyAPIView):
	# RetrieveUpdateDestroyAPIView / RetrieveAPIView
	# field which is looked by serializer while rendering json
	# lookup_field = "pk"	"pk" is the default lookup field in generic view
	queryset = Blog.objects.all().order_by('-timestamp')
	serializer_class = BlogSerializer
	# permission_classes = (IsAuthenticated,)	specify default in settings
	permission_classes = (IsOwnerOrReadOnly,)

	# either use method or queryset
	# def get_queryset(self):
	# 	return Blog.objects.all()

	def get_serializer_context(self, *args, **kwargs):
		return {"request": self.request}


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
		qs = Blog.objects.all().order_by('-timestamp')

		# search method in api
		query = self.request.GET.get('q', None)
		if query is not None:
			qs = qs.filter(
				Q(title__icontains=query) | Q(content__icontains=query)
			).distinct()
		return qs

	# add create as well as list functionality to view
	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

	# adds the post method in allowed methods list
	def post(self, request, *args, **kwargs):
		return self.create(request, *args, **kwargs)

	def get_serializer_context(self, *args, **kwargs):
		return {"request": self.request}

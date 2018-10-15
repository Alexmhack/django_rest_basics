from django.urls import path

from .views import (BlogRUDView, BlogListAPIView)  # , BlogCreateAPIView)

app_name = 'api-postings'

urlpatterns = [
	path('', BlogListAPIView.as_view(), name='blog-list-create'),
	path('<int:pk>', BlogRUDView.as_view(), name='blog-rud'),
	# path('create/', BlogCreateAPIView.as_view(), name='blog-create'),
]

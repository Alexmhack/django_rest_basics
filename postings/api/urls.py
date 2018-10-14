from django.urls import path

from .views import (BlogRUDView, BlogCreateAPIView)

app_name = 'api-postings'

urlpatterns = [
	path('<int:pk>', BlogRUDView.as_view(), name='blog-rud'),
	path('create/', BlogCreateAPIView.as_view(), name='blog-create'),
]

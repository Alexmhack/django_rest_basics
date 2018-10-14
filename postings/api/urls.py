from django.urls import path

from .views import BlogRUDView

app_name = 'api-postings'

urlpatterns = [
	path('<int:pk>', BlogRUDView.as_view(), name='blog-rud'),
]

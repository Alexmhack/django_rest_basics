from django.urls import path

from .views import BlogRUDView

urlpatterns = [
	path('<int:pk>', BlogRUDView.as_view(), name='blog-rud'),
]

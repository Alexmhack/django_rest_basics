from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('api/blog/', include('postings.api.urls', namespace='api-postings')),
]

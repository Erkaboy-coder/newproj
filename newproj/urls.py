from django.urls import include, path
from django.contrib import admin
from newproj.api import router
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('topografiya.urls')),
    path('', include('django.contrib.auth.urls')),
    path('api/', include(router.urls)),
]



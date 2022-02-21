from django.urls import include, path
from django.contrib import admin

from django.conf import settings

from django.views.static import serve
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('topografiya.urls')),
    path('', include('django.contrib.auth.urls')),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),

]



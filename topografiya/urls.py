from django.urls import path, re_path
from django.views.static import serve
from django.conf import settings
from . import views

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^signin/$', views.signin, name='signin'),
    re_path(r'^login/$', views.login, name='login'),
    re_path(r'^logout/$', views.logout, name='logout'),
    re_path(r'^pdoworks/$', views.pdoworks, name='pdoworks'),
    re_path(r'^start/$', views.start, name='start'),
    re_path(r'^show_pdowork/(?P<id>\d+)/$', views.show_pdowork, name='show_pdowork'),
    re_path(r'^topografiya/static/files/(?P<path>.*)', serve, {'document_root': settings.DOCS_ROOT}),
]

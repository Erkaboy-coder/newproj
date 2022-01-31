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
    re_path(r'^allworks/$', views.allworks, name='allworks'),
    re_path(r'^program_works_leader/$', views.program_works_leader, name='program_works_leader'),
    re_path(r'^program_work_form_store/$', views.program_work_form_store, name='program_work_form_store'),
    re_path(r'^program_work_form/(?P<id>\d+)/$', views.program_work_form, name='program_work_form'),
    re_path(r'^program_work_form_edit/(?P<id>\d+)/$', views.program_work_form_edit, name='program_work_form_edit'),
    re_path(r'^history_program_work/$', views.history_program_work, name='history_program_work'),
    re_path(r'^start/$', views.start, name='start'),
    re_path(r'^order_to_pdf$', views.order_to_pdf, name='order_to_pdf'),
    re_path(r'^edit_pdowork_changes/$', views.edit_pdowork_changes, name='edit_pdowork_changes'),
    # worker
    re_path(r'^worker_new_works/$', views.worker_new_works, name='worker_new_works'),
    re_path(r'^polevoy_works/$', views.polevoy_works, name='polevoy_works'),
    # worker
    re_path(r'^show_work$', views.show_work, name='show_work'),
    re_path(r'^recive_work$', views.recive_work, name='recive_work'),
    # re_path(r'^ilova_to_pdf$', views.ilova_to_pdf, name='ilova_to_pdf'),
    re_path(r'^show_pdowork/(?P<id>\d+)/$', views.show_pdowork, name='show_pdowork'),
    re_path(r'^edit_pdowork/(?P<id>\d+)/$', views.edit_pdowork, name='edit_pdowork'),
    re_path(r'^topografiya/static/files/(?P<path>.*)', serve, {'document_root': settings.DOCS_ROOT}),
]

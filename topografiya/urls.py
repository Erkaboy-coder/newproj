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
    re_path(r'^save_order$', views.save_order, name='save_order'),
    re_path(r'^allworks/$', views.allworks, name='allworks'),
    re_path(r'^program_works_leader/$', views.program_works_leader, name='program_works_leader'),
    re_path(r'^program_work_form_store/$', views.program_work_form_store, name='program_work_form_store'),
    re_path(r'^program_work_form/(?P<id>\d+)/$', views.program_work_form, name='program_work_form'),
    re_path(r'^program_work_form_edit/(?P<id>\d+)/$', views.program_work_form_edit, name='program_work_form_edit'),
    re_path(r'^program_work_form_re_sent_to_check/(?P<id>\d+)/$', views.program_work_form_re_sent_to_check, name='program_work_form_re_sent_to_check'),
    re_path(r'^program_work_save_edits/(?P<id>\d+)/$', views.program_work_save_edits, name='program_work_save_edits'),
    re_path(r'^sent_to_check_programwork$', views.sent_to_check_programwork, name='sent_to_check_programwork'),
    re_path(r'^program_work_form_re_sent/(?P<id>\d+)/$', views.program_work_form_re_sent,name='program_work_form_re_sent'),
    re_path(r'^history_program_work/$', views.history_program_work, name='history_program_work'),
    re_path(r'^start/$', views.start, name='start'),
    re_path(r'^order_to_pdf$', views.order_to_pdf, name='order_to_pdf'),
    re_path(r'^doing_program_work_file$', views.doing_program_work_file, name='doing_program_work_file'),
    re_path(r'^doing_akt_komeral_file$', views.doing_akt_komeral_file, name='doing_akt_komeral_file'),
    re_path(r'^edit_pdowork_changes/$', views.edit_pdowork_changes, name='edit_pdowork_changes'),
    re_path(r'^leader_polevoy_works/$', views.leader_polevoy_works, name='leader_polevoy_works'),
    re_path(r'^checking_polevoy_works/(?P<id>\d+)/$', views.checking_polevoy_works, name='checking_polevoy_works'),
    re_path(r'^save_akt_polevoy$', views.save_akt_polevoy, name='save_akt_polevoy'),
    re_path(r'^edit_akt_polevoy$', views.edit_akt_polevoy, name='edit_akt_polevoy'),
    re_path(r'^send_to_kameral$', views.send_to_kameral, name='send_to_kameral'),
    re_path(r'^deny_polevoy$', views.deny_polevoy, name='deny_polevoy'),
    re_path(r'^leader_komeral_works/$', views.leader_komeral_works, name='leader_komeral_works'),
    re_path(r'^leader_komeral_checking/$', views.leader_komeral_checking, name='leader_komeral_checking'),
    re_path(r'^checking_komeral_works/(?P<id>\d+)/$', views.checking_komeral_works, name='checking_komeral_works'),
    re_path(r'^show_komeral_checking_leader/(?P<id>\d+)/$', views.show_komeral_checking_leader, name='show_komeral_checking_leader'),


    re_path(r'^leader_rejected_komeral_works/(?P<id>\d+)/$', views.leader_rejected_komeral_works, name='leader_rejected_komeral_works'),

    re_path(r'^show_komeral_work/(?P<id>\d+)/$', views.show_komeral_work, name='show_komeral_work'),
    re_path(r'^rejected_komeral_works/(?P<id>\d+)/$', views.rejected_komeral_works, name='rejected_komeral_works'),
    re_path(r'^save_akt_komeral$', views.save_akt_komeral, name='save_akt_komeral'),
    re_path(r'^sent_to_check_akt$', views.sent_to_check_akt, name='sent_to_check_akt'),
    re_path(r'^deny_komeral$', views.deny_komeral, name='deny_komeral'),

    # worker
    re_path(r'^worker_new_works/$', views.worker_new_works, name='worker_new_works'),
    re_path(r'^polevoy_works/$', views.polevoy_works, name='polevoy_works'),
    re_path(r'^polevoy_work_doing/(?P<id>\d+)/$', views.polevoy_work_doing, name='polevoy_work_doing'),
    re_path(r'^save_sirie_files/$', views.save_sirie_files, name='save_sirie_files'),
    re_path(r'^save_files$', views.save_files, name='save_files'),
    re_path(r'^store$', views.store, name='store'),
    re_path(r'^edit_poyasitelniy$', views.edit_poyasitelniy, name='edit_poyasitelniy'),
    re_path(r'^send_to_check_polevoy$', views.send_to_check_polevoy, name='send_to_check_polevoy'),
    re_path(r'^send_to_check_komeral$', views.send_to_check_komeral, name='send_to_check_komeral'),
    re_path(r'^edit_sirie_files/(?P<id>\d+)/$', views.edit_sirie_files, name='edit_sirie_files'),
    re_path(r'^object_poyasitelniy_form/(?P<id>\d+)/$', views.object_poyasitelniy_form, name='object_poyasitelniy_form'),

    re_path(r'^worker_komeral_works/$', views.worker_komeral_works, name='worker_komeral_works'),
    re_path(r'^show_rejected_komeral_works/(?P<id>\d+)/$', views.show_rejected_komeral_works, name='show_rejected_komeral_works'),

    re_path(r'^leader_akt_form_edit/(?P<id>\d+)/$', views.leader_akt_form_edit, name='leader_akt_form_edit'),
    re_path(r'^leader_akt_komeral_form_edit/(?P<id>\d+)/$', views.leader_akt_komeral_form_edit, name='leader_akt_komeral_form_edit'),
    re_path(r'^re_send_to_check_komeral$', views.re_send_to_check_komeral, name='re_send_to_check_komeral'),

    # worker

    # geodezist
    re_path(r'^program_works_geodezis/$', views.program_works_geodezis, name='program_works_geodezis'),
    re_path(r'^program_work_event/(?P<id>\d+)/$', views.program_work_event, name='program_work_event'),
    re_path(r'^confirm_program_work$', views.confirm_program_work, name='confirm_program_work'),
    re_path(r'^reject_program_work$', views.reject_program_work, name='reject_program_work'),


    re_path(r'^geodesiz_komeral_works/$', views.geodesiz_komeral_works, name='geodesiz_komeral_works'),
    re_path(r'^show_geodesiz_kameral_work/(?P<id>\d+)/$', views.show_geodesiz_kameral_work, name='show_geodesiz_kameral_work'),
    re_path(r'^geodezis_deny_komeral$', views.geodezis_deny_komeral, name='geodezis_deny_komeral'),
    re_path(r'^geodezis_rejected_komeral_works/(?P<id>\d+)/$', views.geodezis_rejected_komeral_works, name='geodezis_rejected_komeral_works'),
    re_path(r'^geodeziz_show_komeral_work/(?P<id>\d+)/$', views.geodeziz_show_komeral_work, name='geodeziz_show_komeral_work'),
    re_path(r'^sent_to_oggd$', views.sent_to_oggd, name='sent_to_oggd'),
    re_path(r'^geodezis_reports/$', views.geodezis_reports, name='geodezis_reports'),
    re_path(r'^geodezis_report_checking/(?P<id>\d+)/$', views.geodezis_report_checking, name='geodezis_report_checking'),
    re_path(r'^show_report_geodezis/(?P<id>\d+)/$', views.show_report_geodezis, name='show_report_geodezis'),
    re_path(r'^reject_report$', views.reject_report, name='reject_report'),
    re_path(r'^confirm_report$', views.confirm_report, name='confirm_report'),
    re_path(r'^sent_to_print/(?P<id>\d+)/$', views.sent_to_print, name='sent_to_print'),

    # geodezist

    # oogd_reports
    re_path(r'^oogd_reports/$', views.oogd_reports, name='oogd_reports'),
    re_path(r'^report_doing/(?P<id>\d+)/$', views.report_doing, name='report_doing'),
    re_path(r'^report_send$', views.report_send, name='report_send'),
    re_path(r'^confirm_print$', views.confirm_print, name='confirm_print'),
    re_path(r'^show_report/(?P<id>\d+)/$', views.show_report, name='show_report'),
    # oogd_reports

    # ogogdprinter
    re_path(r'^ogogd_printer_works/$', views.ogogd_printer_works, name='ogogd_printer_works'),
    re_path(r'^open_to_print/(?P<id>\d+)/$', views.open_to_print, name='open_to_print'),
    re_path(r'^confirm_print2$', views.confirm_print2, name='confirm_print2'),
    # ogogdprinter

    re_path(r'^history/$', views.history, name='history'),
    re_path(r'^workers/$', views.workers, name='workers'),
    re_path(r'^show_all_works/(?P<id>\d+)/$', views.show_all_works, name='show_all_works'),


    re_path(r'^show_work$', views.show_work, name='show_work'),
    re_path(r'^recive_work$', views.recive_work, name='recive_work'),
    # re_path(r'^ilova_to_pdf$', views.ilova_to_pdf, name='ilova_to_pdf'),
    re_path(r'^show_pdowork/(?P<id>\d+)/$', views.show_pdowork, name='show_pdowork'),
    re_path(r'^edit_pdowork/(?P<id>\d+)/$', views.edit_pdowork, name='edit_pdowork'),
    re_path(r'^topografiya/static/files/(?P<path>.*)', serve, {'document_root': settings.DOCS_ROOT}),



]

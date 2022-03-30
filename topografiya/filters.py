import django_filters

from .models import *

class ObjectsFilter(django_filters.FilterSet):
    class Meta:
        model = WorkerObject
        fields = ['object', 'status']

        # filter_overrides = ['abris_file', 'kroki_file', 'jurnal_file', 'vidimes_file', 'list_agreement_file',
        #                     'topo_plan', 'status_printer', 'status_repoert_printer', 'status_geodezis_komeral', 'active_time']
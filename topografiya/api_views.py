# rest_framework
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import serializers
from .serializers import *

from .models import Worker, Branch

class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all().order_by('id')
    serializer_class = BranchSerializer
    permission_classes = [permissions.AllowAny]

class WorkerViewSet(viewsets.ModelViewSet):
    queryset = Worker.objects.all().order_by('id')
    serializer_class = WorkerSerializer

class ObjectViewSet(viewsets.ModelViewSet):
    queryset = Object.objects.all().order_by('id')
    serializer_class = ObjectSerializer

class PdoViewSet(viewsets.ModelViewSet):
    queryset = PdoWork.objects.all().order_by('id')
    serializer_class = PdoSerializer
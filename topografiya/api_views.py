# rest_framework
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import serializers
from .serializers import *

from .models import Worker, Branch

class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all().order_by('id')
    serializer_class = BranchSerializer
    permission_classes = [permissions.IsAuthenticated]

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all().order_by('id')
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]

class WorkerViewSet(viewsets.ModelViewSet):
    queryset = Worker.objects.all().order_by('id')
    serializer_class = WorkerSerializer
    permission_classes = [permissions.IsAuthenticated]

class ObjectViewSet(viewsets.ModelViewSet):
    queryset = Object.objects.all().order_by('id')
    serializer_class = ObjectSerializer
    permission_classes = [permissions.IsAuthenticated]

class PdoViewSet(viewsets.ModelViewSet):
    queryset = PdoWork.objects.all().order_by('id')
    serializer_class = PdoSerializer
    permission_classes = [permissions.IsAuthenticated]
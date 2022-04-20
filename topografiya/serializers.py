from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class WorkerSerializer(serializers.ModelSerializer):
    branch = BranchSerializer(many=False, read_only=True)
    department = DepartmentSerializer(many=False, read_only=True)
    user = serializers.StringRelatedField(many=False, read_only=True)
    class Meta:
        model = Worker
        fields = '__all__'


class PdoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PdoWork
        fields = '__all__'

class ObjectSerializer(serializers.HyperlinkedModelSerializer):
    pdowork = PdoSerializer(many=False, read_only=True)
    worker = serializers.StringRelatedField(many=False, read_only=True)
    class Meta:
        model = Object
        fields = '__all__'


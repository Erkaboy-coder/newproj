from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *



class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = ['full_name', 'email', 'contact', 'branch','status']
        # fields = ['full_name', 'email', 'contact', 'branch','status']

class BranchSerializer(serializers.ModelSerializer):
    # workerbranch = WorkerSerializer(many=True,read_only=True)
    class Meta:
        model = Branch
        fields = '__all__'

class ObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Object
        fields = '__all__'

class PdoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PdoWork
        fields = '__all__'

from django.urls import include, path
from rest_framework import routers
from topografiya import views, api_views

router = routers.DefaultRouter()
router.register(r'workers', api_views.WorkerViewSet)
router.register(r'branches', api_views.BranchViewSet)
router.register(r'objects', api_views.ObjectViewSet)
router.register(r'pdo', api_views.PdoViewSet)


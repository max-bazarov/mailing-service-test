from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.api.views import ClientViewSet

router = DefaultRouter()
router.register(r'users', ClientViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
]

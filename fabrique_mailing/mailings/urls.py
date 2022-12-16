from django.urls import path, include
from rest_framework.routers import DefaultRouter

from mailings.api.views import MailingViewSet

router = DefaultRouter()
router.register(r'mailings', MailingViewSet, basename='mailings')

urlpatterns = [
    path('', include(router.urls)),
]

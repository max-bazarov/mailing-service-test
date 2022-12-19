from django.urls import include, path
from mailings.api.views import MailingViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'mailings', MailingViewSet, basename='mailings')

urlpatterns = [
    path('', include(router.urls)),
]

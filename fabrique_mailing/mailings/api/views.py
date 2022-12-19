from mailings.api.serializers import MailingSerializer
from mailings.models import Mailing
from rest_framework.viewsets import ModelViewSet


class MailingViewSet(ModelViewSet):
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer

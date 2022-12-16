from rest_framework.viewsets import ModelViewSet

from mailings.api.serializers import MailingSerializer
from mailings.models import Mailing


class MailingViewSet(ModelViewSet):
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer

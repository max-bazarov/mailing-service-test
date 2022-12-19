from rest_framework.viewsets import ModelViewSet

from mailings.api.serializers import MailingSerializer
from mailings.models import Mailing
from mailings.tasks import start_mailing


class MailingViewSet(ModelViewSet):
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer

    def perform_create(self, serializer):
        serializer.save()

        duration = (
            serializer.instance.end_at - serializer.instance.start_at
        ).total_seconds()

        start_mailing.apply_async(
            args=[serializer.instance.id],
            eta=serializer.instance.start_at,
            time_limit=duration
        )

from rest_framework import viewsets, generics
from rest_framework.decorators import action
from rest_framework.response import Response

from mailings.api.serializers import MailingSerializer, MessageSerializer
from mailings.models import Mailing, Message
from mailings.tasks import start_mailing


class MailingViewSet(viewsets.ModelViewSet):
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer

    @action(detail=True)
    def stats(self, request, pk=None):
        messages = self.get_object().messages
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

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


class MessageList(generics.ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        return Message.objects.filter(mailing_id=self.kwargs['mailing_id'])

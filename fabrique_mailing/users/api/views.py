from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet

from users.api.serializers import ClientSerializer

Client = get_user_model()


class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

from core.utils import parse_operator_code
from core.validators import validate_phone_number
from django.contrib.auth import get_user_model
from rest_framework import serializers
from timezone_field.rest_framework import TimeZoneSerializerField
from users.models import OperatorCode, Tag

Client = get_user_model()


class CustomSlugRelatedField(serializers.SlugRelatedField):
    def to_internal_value(self, data):
        obj, _ = self.get_queryset().get_or_create(**{self.slug_field: data})
        return obj


class ClientSerializer(serializers.ModelSerializer):
    operator_code = serializers.SlugRelatedField(
        slug_field='code',
        read_only=True
    )
    tag = CustomSlugRelatedField(
        slug_field='name',
        queryset=Tag.objects.all(),
        required=False
    )
    time_zone = TimeZoneSerializerField(use_pytz=True)

    class Meta:
        model = Client
        fields = (
            'phone_number',
            'operator_code',
            'tag',
            'time_zone'
        )

    def validate_phone_number(self, value):
        return validate_phone_number(value)

    def create(self, validated_data):
        phone_number = validated_data.pop('phone_number')
        operator_code = parse_operator_code(phone_number)
        operator_code, _ = OperatorCode.objects.get_or_create(
            code=operator_code
        )
        time_zone = validated_data.pop('time_zone')

        if 'tag' not in self.initial_data:
            client = Client.objects.create(
                phone_number=phone_number,
                operator_code=operator_code,
                time_zone=time_zone
            )
            return client

        tag = validated_data.pop('tag')
        current_tag, _ = Tag.objects.get_or_create(name=tag)

        client = Client.objects.create(
            phone_number=phone_number,
            operator_code=operator_code,
            tag=current_tag,
            time_zone=time_zone
        )

        return client

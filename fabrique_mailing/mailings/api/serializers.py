import datetime

from rest_framework import serializers

from mailings.models import Mailing
from users.models import Filter, OperatorCode, Tag


class FilterSerializer(serializers.ModelSerializer):
    tag = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Tag.objects.all()
    )
    operator_code = serializers.SlugRelatedField(
        slug_field='code',
        queryset=OperatorCode.objects.all()
    )

    class Meta:
        model = Filter
        fields = ('tag', 'operator_code')


class MailingSerializer(serializers.ModelSerializer):
    filter = FilterSerializer()

    class Meta:
        model = Mailing
        fields = ('message', 'start_at', 'end_at', 'filter')

    def validate_start_at(self, data):
        if data.timestamp() < datetime.datetime.now().timestamp():
            raise serializers.ValidationError(
                'Start time must be in the future'
            )
        return data

    def validate_end_at(self, data):
        if data.timestamp() < datetime.datetime.now().timestamp():
            raise serializers.ValidationError(
                'End time must be in the future'
            )
        return data

    def create(self, validated_data):
        filter_data = validated_data.pop('filter')
        try:
            filter = Filter.objects.get(**filter_data)
        except Filter.DoesNotExist:
            try:
                tag = Tag.objects.get(name=filter_data['tag'])
            except Tag.DoesNotExist:
                raise serializers.ValidationError('Tag does not exist')

            try:
                operator_code = OperatorCode.objects.get(
                    code=filter_data['operator_code']
                )
            except OperatorCode.DoesNotExist:
                raise serializers.ValidationError(
                    'OperatorCode does not exist'
                )

            filter = Filter.objects.create(
                tag=tag,
                operator_code=operator_code)

        mailing = Mailing.objects.create(filter=filter, **validated_data)

        return mailing

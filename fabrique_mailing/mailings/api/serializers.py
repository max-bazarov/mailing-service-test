from rest_framework import serializers

from mailings.models import Mailing, MailingTag
from users.models import Tag


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('name',)


class MailingSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = Mailing
        fields = ('message', 'start_at', 'end_at', 'tags')

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        mailing = Mailing.objects.create(**validated_data)

        for tag in tags:
            try:
                tag = Tag.objects.get(**tag)
            except Tag.DoesNotExist:
                raise serializers.ValidationError('Tag does not exist')

            MailingTag.objects.create(mailing=mailing, tag=tag)

        return mailing

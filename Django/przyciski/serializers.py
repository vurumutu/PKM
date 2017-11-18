from rest_framework import serializers
from przyciski.models import TrainRequest#, DEVICE_TYPE_ENUM
# from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES


class PrzyciskiSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    DEVICE_TYPE_ENUM = (
    ('0', 'WebPage'),
    ('1', 'AndroidApp'),
    )

    device_type = serializers.CharField(max_length=1)#, choices=DEVICE_TYPE_ENUM)
    velocity = serializers.IntegerField(
        default=0)
		
    train_identificator = serializers.IntegerField(
        default=1)
    

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return przyciski.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.id = validated_data.get('id', instance.id)
        instance.device_type = validated_data.get('device_type', instance.device_type)
        instance.velocity = validated_data.get('velocity', instance.velocity)
        instance.train_identificator = validated_data.get('train_identificator', instance.train_identificator)

		
        instance.save()
        return instance
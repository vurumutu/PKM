from rest_framework import serializers
from przyciski.models import TrainRequest#, DEVICE_TYPE_ENUM
# from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES


class PrzyciskiSerializer(serializers.Serializer):
    # id = serializers.IntegerField(read_only=True)
    # title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    # code = serializers.CharField(style={'base_template': 'textarea.html'})
    # linenos = serializers.BooleanField(required=False)
    # language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
    # style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')


    DEVICE_TYPE_ENUM = (
    ('0', 'WebPage'),
    ('1', 'AndroidApp'),
    )

    device_type = serializers.CharField(max_length=1)#, choices=DEVICE_TYPE_ENUM)
    velocity = serializers.IntegerField(
        default=0)#,
        #validators=[MaxValueValidator(50), MinValueValidator(-50)]
    #)
    train_identificator = serializers.IntegerField(
        default=1)#,
        #validators=[MaxValueValidator(2), MinValueValidator(0)]
    #)
    

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return przyciski.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.device_type = validated_data.get('device_type', instance.device_type)
        instance.velocity = validated_data.get('velocity', instance.velocity)
        instance.train_identificator = validated_data.get('train_identificator', instance.train_identificator)

        # instance.title = validated_data.get('title', instance.title)
        # instance.code = validated_data.get('code', instance.code)
        # instance.linenos = validated_data.get('linenos', instance.linenos)
        # instance.language = validated_data.get('language', instance.language)
        # instance.style = validated_data.get('style', instance.style)

        instance.save()
        return instance
from rest_framework import serializers
from przyciski.models import TrainRequest#, DEVICE_TYPE_ENUM
# from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES

class PostPrzyciskiSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)

    DEVICE_TYPE_ENUM = (
    ('0', 'WebPage'),
    ('1', 'AndroidApp'),
    )

    device_type = serializers.CharField(max_length=1)#, choices=DEVICE_TYPE_ENUM)
    velocity = serializers.IntegerField(default=0)
		
    train_identificator = serializers.IntegerField(default=1)
    

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

class PrzyciskiSerializer(serializers.Serializer):

    #     id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    # velocity = models.IntegerField(
    #     default=0,
    #     validators=[MaxValueValidator(127), MinValueValidator(-127)]
    # )
    # train_identificator = models.IntegerField(
    #     default=1,
    #     validators=[MaxValueValidator(10), MinValueValidator(1)]
    # )
    
    # position = models.IntegerField(
    #     default=0,
    #     validators=[MinValueValidator(0), MaxValueValidator(10000)]
    # )
    # track_number = models.IntegerField(
    #     default=1,
    #     validators=[MinValueValidator(1), MaxValueValidator(4)]
    # )


    id = serializers.IntegerField(read_only=True)
    velocity = serializers.IntegerField(default=0)
    train_identificator = serializers.IntegerField(default=1)
    position = serializers.IntegerField(default=0)
    track_number = serializers.IntegerField(default=1)

    

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
        instance.velocity = validated_data.get('velocity', instance.velocity)
        instance.train_identificator = validated_data.get('train_identificator', instance.train_identificator)
        instance.position = validated_data.get('position', instance.position)
        instance.track_number = validated_data.get('track_number', instance.track_number)


		
        instance.save()
        return instance
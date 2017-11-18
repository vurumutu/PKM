# Create your models here.
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

DEVICE_TYPE_ENUM = (
('0', 'WebPage'),
('1', 'AndroidApp'),
)


class TrainRequest(models.Model):

	device_type = models.CharField(max_length=1, choices=DEVICE_TYPE_ENUM)
	velocity = models.IntegerField(
		default=0,
		validators=[MaxValueValidator(127), MinValueValidator(-127)]
	)
	train_identificator = models.IntegerField(
		default=1,
		validators=[MaxValueValidator(2), MinValueValidator(0)]
	)
	
	def __str__(self):
		return "Train"#str('Pociag: ',self.device_type)
	

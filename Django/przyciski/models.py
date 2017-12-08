#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Create your models here.
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

DEVICE_TYPE_ENUM = (
('0', 'WebPage'),
('1', 'AndroidApp'),
)

class AvailableTrain(models.Model):
	id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
	velocity = models.IntegerField(
		default=0,
		validators=[MaxValueValidator(127), MinValueValidator(-127)]
	)
	train_identificator = models.IntegerField(
		default=1,
		validators=[MaxValueValidator(2), MinValueValidator(0)]
	)
	
	def __str__(self):
		return "Pociąg numer "+str(self.train_identificator) + ". Jadący z prędkością: " + str(self.velocity)
		
	def change_velocity():
		pass


class TrainRequest(models.Model):
	id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
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
		return "Żądanie dla pociągu numer "+str(self.train_identificator) + ". Żądana prędkość: " + str(self.velocity)
		

	

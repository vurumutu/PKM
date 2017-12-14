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
	#aktualna predkosc pociagu
	velocity = models.IntegerField(
		default=0,
		validators=[MaxValueValidator(127), MinValueValidator(-127)]
	)
	#numer pociagu
	train_identificator = models.IntegerField(
		default=1,
		validators=[MaxValueValidator(10), MinValueValidator(1)]
	)
	# pozycja na danym torze
	position = models.IntegerField(
		default=0,
		validators=[MinValueValidator(0), MaxValueValidator(10000)]
	)
	#numer toru
	track_number = models.IntegerField(
		default=1,
		validators=[MinValueValidator(1), MaxValueValidator(4)]
	)
	
	def __str__(self):
		return "Pociag numer "+str(self.train_identificator) + ". Jadacy z predkoscia: " + str(self.velocity)
		
	def change_velocity():
		pass


class TrainRequest(models.Model):
	id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
	# czy wyslano z pc czy telefonu
	device_type = models.CharField(max_length=1, choices=DEVICE_TYPE_ENUM)
	# zadana predkosc
	velocity = models.IntegerField(
		default=0,
		validators=[MaxValueValidator(127), MinValueValidator(-127)]
	)
	# numer pociag
	train_identificator = models.IntegerField(
		default=1,
		validators=[MaxValueValidator(2), MinValueValidator(0)]
	)
	
	# czy wykonano rozkaz
	was_carried_out = models.BooleanField() # czy wykonano rozkaz
	
	def __str__(self):
		return "Zadanie dla pociagu numer "+str(self.train_identificator) + ". Zadana predkosc: " + str(self.velocity)
		

	

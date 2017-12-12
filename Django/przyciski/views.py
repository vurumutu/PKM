# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response,render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import TrainRequest, AvailableTrain
from django.template import RequestContext, Template

#form
import pade
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django import forms

from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from przyciski.serializers import PrzyciskiSerializer

#import xpressnet
from xpressnet import Client, Train
from time import sleep

import agent
import czyWolny

from pade.misc.utility import display_message
from pade.misc.common import set_ams, start_loop
from pade.core.agent import Agent
from pade.acl.aid import AID

TCP_IP = '192.168.210.200'
TCP_PORT = 5550


def obslugaAgentowa (nr):
	agentsList = list()

	for i in range(len(AvailableTrain.objects.all())): #tworzymy tyle agentow, ile jest pociagow w bazie
		print (i)
		t = AvailableTrain.objects.get(train_identificator=nr)
		sector = t.position
		track = t.track_number
		agente_train = agent.AgenteHelloWorld(AID(name='agente_hello'), [sector,track])
		agentsList.append(agente_train)

	message = agentsList[nr].newOrder() #czyli agent ktory otrzymal rozkaz

	for i in range(len(AvailableTrain.objects.all())):
		if i != nr: #odpowiadaja pozostale
			agentsList[i].react(message)	

	#checkLinesAvaliability() nr, [] - sektor startu odczytany z poc(nr), [] - cel, lista[x,y]

	wolne = True # True

	return wolne	

def home (request):
	print('')
	print(str(request))
	print('')

	client = Client()
	client.connect(TCP_IP, TCP_PORT)

	if request.method == 'POST':

		if 'stop_trains' in request.POST:
			# wez wszystkie pociag
			availableTrains = AvailableTrain.objects.all()
			# ustaw predkosc kazdego na zero
			for at in availableTrains:
				at.velocity = 0
				at.save()
				#TODO send request

			# Kod odpowiedzialny za zatrzymanie pociągów, aktualnie zatrzymywany jest tylko pociąg 5
			#TODO pobrać listę pociągów z bazy Django i w pętli zadać im prędkość 0 analogicznie do poniższego kodu
			train_number = 5
			train = Train(train_number)
			msg = train.move(0)
			client.send(msg)

			availableTrains = AvailableTrain.objects.all()
			return render(request, 'stronka.html',{'availableTrains': availableTrains})

		elif 'trains_list' in request.POST:

			# Pobieranie listy pociągów ze sterownika
			address = 0
			while True:
				msg = client.get_next_address_in_stack(address)
				rec = client.send(msg)
				print(rec)
				if rec[3] is '0':
					print("Znaleziony adres lokomotywy: " + rec[7:8])
					AvailableTrain.objects.create(
						train_identificator= int(rec[7:8], 16),
						velocity=0,
						position = 1,
						track_number = 0
					)
					address = int(rec[4:8], 16)
					msg = client.get_locomotive_status(address)
					rec2 = client.send(msg)
					rec2 = bin(int(rec, 16))[2:]
				else:
        			 break
				sleep(1)

			availableTrains = AvailableTrain.objects.all()
			return render(request, 'stronka.html',{'availableTrains': availableTrains})
				#TODO Dodac kod na pobranie listy pociagow tutaj
		#Sterowanie
		else:
			new_train_request = request.POST #['new_train']

			user = User.objects.first()  # TODO: get the currently logged in user
			
			print(new_train_request.get("page_velocity"))
			
			nr = new_train_request.get("train_number")
			t = AvailableTrain.objects.get(train_identificator=nr)
			print(int(nr), t)
			
			wolne = obslugaAgentowa(int(nr))

			if wolne:
				new_created_train = TrainRequest.objects.create(
					train_identificator= new_train_request.get("train_number"),
					velocity=new_train_request.get("page_velocity"),
					was_carried_out = 1,
					device_type = 0
				)
				t.velocity = new_train_request.get("page_velocity")  # change field
				t.save() # this will update only

				# zadawanie prędkości pociągom
				train = Train(int(nr))
				if int(t.velocity) >= 0:
					direction = 1
				else:
					direction = 0
				msg = train.move(abs(int(t.velocity)), direction)
				client.send(msg)

			else:
				new_created_train = TrainRequest.objects.create(
					train_identificator= new_train_request.get("train_number"),
					velocity=new_train_request.get("page_velocity"),
					was_carried_out = 1,
					device_type = 0
				)
				print ("Rozkaz zabroniony. Tor zablokowany")
				t.velocity = 0
				t.save()
			#TODO send request

	availableTrains = AvailableTrain.objects.all()
	return render(request, 'stronka.html',{'availableTrains': availableTrains})
	
def main_home_page(request):
	trainRequests = TrainRequest.objects.all()
	availableTrains = AvailableTrain.objects.all()
	return render(request, 'homepage.html',{'trainRequests' : trainRequests, 'availableTrains': availableTrains})


@csrf_exempt
def przyciski_list(request):
	"""
	List all code snippets, or create a new snippet.
	"""
	if request.method == 'GET':
		przyciski = AvailableTrain.objects.all()
		serializer = PrzyciskiSerializer(przyciski, many=True)
		return JsonResponse(serializer.data, safe=False)

	elif request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = PrzyciskiSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data, status=201)
		return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def przyciski_detail(request, _pk):
	"""
	Retrieve, update or delete a code snippet.
	"""
	print(_pk)
	try:
		lista_przyciski = list(TrainRequest.objects.all())#get(pk=_pk)
		przyciski = lista_przyciski[int(_pk)]
	except:# TrainRequest.DoesNotExist: #Exception as e:#TrainRequest.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		serializer = PrzyciskiSerializer(przyciski)
		return JsonResponse(serializer.data)

	elif request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = PostPrzyciskiSerializer(przyciski, data=data)
		print('bla')
		if serializer.is_valid():
			print('123')
			serializer.save()
			return JsonResponse(serializer.data)
		return JsonResponse(serializer.errors, status=400)

	elif request.method == 'DELETE':
		przyciski.delete()
		return HttpResponse(status=204)
		
@csrf_exempt
def przyciski_posting(request):
	"""
	Retrieve, update or delete a code snippet.
	"""
	#try:
	#    lista_przyciski = list(TrainRequest.objects.all())#get(pk=_pk)
	#    przyciski = lista_przyciski[int(_pk)]
	#except:# TrainRequest.DoesNotExist: #Exception as e:#TrainRequest.DoesNotExist:
	#    return HttpResponse(status=404)

	#if request.method == 'GET':
	#    serializer = PrzyciskiSerializer(przyciski)
	#    return JsonResponse(serializer.data)

	if request.method == 'PUT':
		data = JSONParser().parse(request)
		serializer = PrzyciskiSerializer(przyciski, data=data)
		print('bla')
		if serializer.is_valid():
			print('123')
			serializer.save()
			return JsonResponse(serializer.data)
		return JsonResponse(serializer.errors, status=400)

	elif request.method == 'DELETE':
		#przyciski.delete()
		return HttpResponse(status=204)
		
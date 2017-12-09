# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response,render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import TrainRequest, AvailableTrain
from django.template import RequestContext, Template

#form
#import pade
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django import forms

from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from przyciski.serializers import PrzyciskiSerializer

#import agent

from pade.misc.utility import display_message
from pade.misc.common import set_ams, start_loop
from pade.core.agent import Agent
from pade.acl.aid import AID

def obslugaAgentowa (nr):
	agentsList = list()

	for i in range(len(AvailableTrain.objects.all())): #tworzymy tyle agentow, ile jest pociagow w bazie
		print (i)
		agente_train = agent.AgenteHelloWorld(AID(name='agente_hello'), [1,1]) #kazdemu zamiast [1, 1] powinnismy przypisywac sektor w jakim sie znajduje, ale nie wiem, skad to wytrzasnac
		agentsList.append(agente_train)

	message = agentsList[nr].newOrder() #czyli agent ktory otrzymal rozkaz

	for i in range(len(AvailableTrain.objects.all())):
		if i != nr: #odpowiadaja pozostale
			agentsList[i].react(message)	
	
	#tu bedzie dodane sprawdzanie czy nic nie stoi na drodze
	#zakladamy, ze nic, wiec:
	wolne = False # True

	return wolne	

def home (request):
	if request.method == 'POST':
		if 'stop_trains' in request.POST:
			return render(request,'stronka.html')
				#TODO Dodac kod na zatrzymanie wszystkich pociągow tutaj
		elif 'trains_list' in request.POST:
			return render(request,'stronka.html')
				#TODO Dodac kod na pobranie listy pociągow tutaj
		else:
			new_train_request = request.POST #['new_train']

			user = User.objects.first()  # TODO: get the currently logged in user
			
			new_created_train = TrainRequest.objects.create(
				train_identificator= new_train_request.get("train_number"),
				velocity=new_train_request.get("page_velocity"),
				device_type = 0
			)
			
			nr = new_train_request.get("train_number")
			t = AvailableTrain.objects.get(id=nr)
			print(int(nr), t)
			
			wolne = obslugaAgentowa(int(nr))

			if wolne:
				t.velocity = new_train_request.get("page_velocity")  # change field
				t.save() # this will update only

			else:
				print ("Rozkaz zabroniony. Tor zablokowany")
				t.velocity = 0
				t.save()

	trainRequests = TrainRequest.objects.all()
	availableTrains = AvailableTrain.objects.all()
	print(availableTrains)
	return render(request, 'stronka.html',{'trainRequests' : trainRequests, 'availableTrains': availableTrains})
	
def main_home_page(request):
	trainRequests = TrainRequest.objects.all()
	availableTrains = AvailableTrain.objects.all()
	print(availableTrains)
	return render(request, 'homepage.html',{'trainRequests' : trainRequests, 'availableTrains': availableTrains})


@csrf_exempt
def przyciski_list(request):
	"""
	List all code snippets, or create a new snippet.
	"""
	if request.method == 'GET':
		przyciski = TrainRequest.objects.all()
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

	elif request.method == 'PUT':
		data = JSONParser().parse(request)
		serializer = PrzyciskiSerializer(przyciski, data=data)
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
		przyciski.delete()
		return HttpResponse(status=204)
		
		
from django.shortcuts import render_to_response,render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import TrainRequest
from django.template import RequestContext, Template

#form
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django import forms

from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from przyciski.serializers import PrzyciskiSerializer

def home (request):
	if request.method == 'POST':
		new_train_request = request.POST #['new_train']

		user = User.objects.first()  # TODO: get the currently logged in user

		new_created_train = TrainRequest.objects.create(
			train_identificator= new_train_request.get("train_number"),
			velocity=new_train_request.get("page_velocity"),
			device_type = 0
		)

	return render(request,'stronka.html')
	
def main_home_page(request):
	trainRequests = TrainRequest.objects.all()
	return render(request, 'homepage.html',{'trainRequests' : trainRequests})


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
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        przyciski.delete()
        return HttpResponse(status=204)
		
		
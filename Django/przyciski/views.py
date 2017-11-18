from django.shortcuts import render_to_response,render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import TrainRequest
from django.template import RequestContext, Template

#form
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django import forms

#from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
#from przyciski.models import przyciski
from przyciski.serializers import PrzyciskiSerializer

def home (request):
	#train_request = get_object_or_404(TrainRequest, pk=pk)

	if request.method == 'POST':
		new_train_request = request.POST #['new_train']
		print(new_train_request)

		user = User.objects.first()  # TODO: get the currently logged in user

		new_created_train = TrainRequest.objects.create(
			train_identificator= new_train_request.get("train_number"),
			velocity=new_train_request.get("page_velocity"),
			device_type = 0
		)

		#return redirect('przyciski')#, pk=board.pk)  # TODO: redirect to the created topic page

    #return render(request, 'new_topic.html', {'board': board})
	return render(request,'stronka.html')#,{'train': train})
	
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
def przyciski_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        przyciski = TrainRequest.objects.get(pk=pk)
    except TrainRequest.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SnippetSerializer(przyciski)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = PrzyciskiSerializer(przyciski, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        przyciski .delete()
        return HttpResponse(status=204)
		
		
def new_train_request(request, pk):
    train_request = get_object_or_404(train_request, pk=pk)

    if request.method == 'POST':
        subject = request.POST['subject']
        message = request.POST['message']

        user = User.objects.first()  # TODO: get the currently logged in user

        topic = Topic.objects.create(
            subject=subject,
            board=board,
            starter=user
        )

        post = Post.objects.create(
            message=message,
            topic=topic,
            created_by=user
        )

        return redirect('board_topics', pk=board.pk)  # TODO: redirect to the created topic page

    return render(request, 'new_topic.html', {'board': board})
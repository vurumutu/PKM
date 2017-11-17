from django.shortcuts import render_to_response
from django.http import HttpResponse, JsonResponse
from .models import TrainRequest

#from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
#from przyciski.models import przyciski
from przyciski.serializers import PrzyciskiSerializer

def home (request):
    #return HttpResponse('Hello, World!')
    return render_to_response('stronka.html')
	
def main_home_page(requst):
	trainRequests = TrainRequest.objects.all()
	return render_to_response('homepage.html',{'trainRequests' : trainRequests})


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
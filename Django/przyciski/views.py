from django.shortcuts import render_to_response
from django.http import HttpResponse
from .models import TrainRequest

def home (request):
    #return HttpResponse('Hello, World!')
    return render_to_response('stronka.html')
	
def main_home_page(requst):
	trainRequests = TrainRequest.objects.all()
	return render_to_response('homepage.html',{'trainRequests' : trainRequests})
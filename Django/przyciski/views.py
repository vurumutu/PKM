from django.shortcuts import render_to_response
from django.http import HttpResponse

def home (request):
    #return HttpResponse('Hello, World!')
    return render_to_response('stronka.html')
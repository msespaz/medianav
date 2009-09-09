# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext

def default(request):
    return render_to_response('default.html', locals(), context_instance=RequestContext(request))


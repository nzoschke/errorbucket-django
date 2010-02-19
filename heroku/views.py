from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils import simplejson

def resources(request):
  result = {'id': 1}
  return HttpResponse(simplejson.dumps(result), mimetype='application/json')
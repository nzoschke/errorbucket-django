from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils import simplejson
from errorbucket.auth.decorators import http_auth_required

@http_auth_required({'heroku': '20c0c5b319542acc'})
def resources(request):
  result = {'id': 1}
  return HttpResponse(simplejson.dumps(result), mimetype='application/json')
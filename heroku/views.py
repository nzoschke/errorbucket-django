import uuid

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import simplejson
from errorbucket.auth.decorators import http_auth_required

from django.contrib.auth.models import User
from errorbucket.buckets.models import Bucket

@http_auth_required({'heroku': '20c0c5b319542acc'})
def resources(request):
  randomness = str(uuid.uuid4()).split('-')
  user = User.objects.create_user('heroku-%s' % randomness[0], '', randomness[1])
  bucket = Bucket.objects.create(user=user, name='heroku')
  result = { "id": user.id, "config": { "ERRORBUCKET_API_KEY": bucket.api_key } }
  return HttpResponse(simplejson.dumps(result), mimetype='application/json')
  
@http_auth_required({'heroku': '20c0c5b319542acc'})
def resource(request, id):
  user = get_object_or_404(User, pk=id)
  user.delete()
  return HttpResponse('ok')
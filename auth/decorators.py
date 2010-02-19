import base64
from functools import wraps
from django.http import HttpResponse

class http_auth_required(object):
  """
  A decorator to handle basic HTTP authentication. Takes a dictionary of
  username: password pairs to authenticate against. Example:

  @http_auth_required({'fred': 'passwd'})
  def resources(request):
    return HttpResponse('welcome %s' % request.META['REMOTE_USER']) # => 'welcome fred'
  """
  def __init__(self, credentials={}):
    self.credentials = credentials

  def __call__(self, view):
    def inner(request, *args, **kwargs):
      # header indicates login attempt
      if request.META.has_key('HTTP_AUTHORIZATION'):
        auth = request.META['HTTP_AUTHORIZATION'].split()
        if len(auth) == 2 and auth[0].lower() == 'basic':
            username, password = base64.b64decode(auth[1]).split(':')
            if self.credentials.has_key(username) and self.credentials[username] == password:
              request.META['REMOTE_USER'] = username
              return view(request, *args, **kwargs)

      # The credentials are incorrect, or not provided; challenge for username/password
      response = HttpResponse()
      response.status_code = 401
      response['WWW-Authenticate'] = 'Basic realm="restricted"'
      return response

    return inner
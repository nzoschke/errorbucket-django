from django.conf.urls.defaults import *

urlpatterns = patterns('errorbucket.heroku.views',
  (r'^resources$', 'resources'),
  (r'^resources/(?P<id>[\d]+)$', 'resource'),
)

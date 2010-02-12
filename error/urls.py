from django.conf.urls.defaults import *

urlpatterns = patterns('errorbucket.error.views',
    (r'^$', 'index'),
    (r'^(?P<name>\w+)/errors/$', 'errors'),
)

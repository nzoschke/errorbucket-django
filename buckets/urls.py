from django.conf.urls.defaults import *

urlpatterns = patterns('errorbucket.buckets.views',
    (r'^$', 'index'),
    (r'^(?P<name>\w+)/errors/$', 'errors'),
)

from django.conf.urls.defaults import *

urlpatterns = patterns('errorbucket.buckets.views',
    (r'^$', 'buckets'),
    (r'^(?P<name>\w+)/$', 'bucket'),
    (r'^(?P<name>\w+)/errors/$', 'errors'),
)

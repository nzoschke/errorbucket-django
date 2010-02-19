from django.contrib import admin
from errorbucket.buckets.models import Bucket, Error

admin.site.register(Bucket)
admin.site.register(Error)
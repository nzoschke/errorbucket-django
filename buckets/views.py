from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.utils import simplejson

from errorbucket.buckets.models import Bucket, Error
from errorbucket.buckets.forms import LoginSignupForm, BucketForm

def is_json(request):
    return 'application/json' in request.META.get('HTTP_ACCEPT', '')

def index(request):
    if request.method == 'POST':
        form = LoginSignupForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/buckets/')
    else:
        form = LoginSignupForm()

    return render_to_response('index.html', {'form': form})

@login_required
def buckets(request):
    if request.method == 'POST':
        form = BucketForm(request.POST, instance=Bucket(user=request.user))
        if form.is_valid():
            form.save()
            if is_json(request):
                return HttpResponse(form.instance.to_json(), mimetype='application/json')
            return HttpResponseRedirect('/buckets/')
    else:
        form = BucketForm()
    return render_to_response('buckets.html', {'buckets': request.user.bucket_set.all(), 'form': form})

def errors(request, name):
    # requires API KEY or session for authentication
    try:
        if request.POST.has_key('api_key'):
            bucket = Bucket.objects.get(api_key=request.POST['api_key'], name=name)
        else:
            bucket = Bucket.objects.get(user=request.user, name=name)
    except Exception:
        return HttpResponse(status=401) # unauthorized

    # create or get errors
    if request.method == 'POST':
        e = Error.objects.create(bucket=bucket, message=request.POST['message'])
        if is_json(request):
            return HttpResponse(e.to_json(), mimetype='application/json')

    elif request.method == 'GET':
        errors = bucket.error_set.all()[:30]
        errors = [error.to_dict() for error in errors]
        return HttpResponse(simplejson.dumps(errors), mimetype='application/json')
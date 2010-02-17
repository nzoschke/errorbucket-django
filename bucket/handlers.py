import os
import uuid
from google.appengine.ext import webapp
from google.appengine.ext import db
from bucket.models import Bucket, Error
from django.utils import simplejson

# TODO
class JSONHandler(webapp.RequestHandler):
  pass
  
class BucketsHandler(webapp.RequestHandler):
  def post(self):
    bucket = Bucket.put_new()
    self.response.out.write(bucket.to_json())
    self.response.headers.add_header("Content-Type", "application/json")

  def get(self):
    b = [bucket.to_dict() for bucket in db.GqlQuery("SELECT * FROM Bucket").fetch(30)]
    self.response.out.write(simplejson.dumps(b))
    self.response.headers.add_header("Content-Type", "application/json")
    

class BucketHandler(webapp.RequestHandler):
  def get(self, key_name):
    bucket = Bucket.get_by_key_name(key_name)
    if not bucket:
      self.error(404)
      return
      
    e = [error.to_dict() for error in bucket.error_set.fetch(30)]
    self.response.out.write(simplejson.dumps(e))
    self.response.headers.add_header("Content-Type", "application/json")
      
  def post(self, key_name):
    bucket = Bucket.get_by_key_name(key_name)
    if not bucket:
      self.error(404)
      return
      
    if bucket.secret_key != self.request.get('secret_key', False):
      self.error(401)
      return
      
    Error(bucket=bucket, message=self.request.get('message', '')).put()
    self.response.out.write(simplejson.dumps('ok'))
    self.response.headers.add_header("Content-Type", "application/json")
    
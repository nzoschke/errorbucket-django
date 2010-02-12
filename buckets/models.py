import uuid

from django.db import models
from django.contrib.auth.models import User
from django.utils import simplejson

class Bucket(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=50)
    api_key = models.CharField(max_length=36, unique=True)

    def reset_api_key(self):
        self.api_key = str(uuid.uuid4())

    def save(self, force_insert=False, force_update=False, using=None):
        if not self.api_key:
            self.reset_api_key()
        super(Bucket, self).save(force_insert, force_update, using)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "api_key": self.api_key}

    def to_json(self):
        return simplejson.dumps(self.to_dict())

class Error(models.Model):
    bucket = models.ForeignKey(Bucket)
    message = models.TextField()

    def to_dict(self):
        return {"id": self.id, "message": self.message,}

    def to_json(self):
        return simplejson.dumps(self.to_dict())

from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import TestCase
from django.test.client import Client
from django.utils import simplejson

from errorbucket.buckets.models import Bucket, Error

class BucketsTest(TestCase):
    def setUp(self):
        self.brian = User.objects.create_user("brian", "brian@example.com", "buckethead")

    def tearDown(self):
        pass

    def test_create_bucket(self):
        b = Bucket.objects.create(user=self.brian)
        self.assertEqual(b.user, self.brian)
        self.assertTrue(b.api_key)

    def test_bucket_enforces_unique_api_key(self):
        Bucket.objects.create(user=self.brian, api_key='123')
        self.assertRaises(IntegrityError, Bucket.objects.create, user=self.brian, api_key='123')

    def test_create_error(self):
        b = Bucket.objects.create(user=self.brian)
        e = Error.objects.create(bucket=b, message="an Exception occurred in line 20...")
        self.assertEqual(e.bucket, b)
        self.assertEqual(1, b.error_set.count())

class BucketsViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.brian = User.objects.create_user("brian", "brian@example.com", "buckethead")
        self.bucket = Bucket.objects.create(user=self.brian, name='app1')

    def tearDown(self):
        pass

    def test_authenticated_json_api(self):
        self.client.login(username='brian', password='buckethead')
        response = self.client.post('/buckets/', {'name': 'app2'}, HTTP_ACCEPT='application/json')
        bucket = simplejson.loads(response.content)
        self.assertEqual('app2', bucket['name'])
        self.assertTrue(bucket['api_key'])

        self.client.post('/buckets/app2/errors/', {'message': 'an error occurred'}, HTTP_ACCEPT='application/json')
        self.client.post('/buckets/app2/errors/', {'message': 'another  error occurred'}, HTTP_ACCEPT='application/json')
        response = self.client.get('/buckets/app2/errors/', HTTP_ACCEPT='application/json')
        errors = simplejson.loads(response.content)
        self.assertEqual(2, len(errors))

    def test_public_json_api(self):
        response = self.client.post('/buckets/app1/errors/', {'message': 'an error occurred'})
        self.assertEqual(401, response.status_code)

        response = self.client.post('/buckets/app1/errors/', {'api_key': 'wrong', 'message': 'an error occurred'})
        self.assertEqual(401, response.status_code)

        response = self.client.post('/buckets/app1/errors/', {'api_key': self.bucket.api_key, 'message': 'an error occurred'}, HTTP_ACCEPT='application/json')
        response = self.client.post('/buckets/app1/errors/', {'api_key': self.bucket.api_key, 'message': 'another  error occurred'}, HTTP_ACCEPT='application/json')
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, self.bucket.error_set.count())

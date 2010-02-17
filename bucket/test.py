import unittest
from rest_client.restful_lib import Connection
from django.utils import simplejson

class BucketsTest(unittest.TestCase):
  def setUp(self):
    self.conn = Connection("http://localhost:8080")
    
  def test_get(self):
    response = self.conn.request_get('/bucket', headers={'Accept': 'application/json'})
    bucket = simplejson.loads(response['body'])
    self.assertTrue(len(bucket) > 0)
    
  def test_post(self):
    response = self.conn.request_post('/bucket', headers={'Accept': 'application/json'})
    bucket = simplejson.loads(response['body'])
    self.assertTrue(bucket['key'])
    self.assertTrue(bucket['secret_key'])

class BucketTest(unittest.TestCase):
  def setUp(self):
    self.conn = Connection("http://localhost:8080")
    response = self.conn.request_get('/bucket', headers={'Accept': 'application/json'})
    self.bucket = simplejson.loads(response['body'])[0]
    self.bucket_url = '/bucket/%s' % self.bucket['key']

  def test_get(self):
    response = self.conn.request_get(self.bucket_url, headers={'Accept': 'application/json'})
    bucket = simplejson.loads(response['body'])
    self.assertTrue(len(bucket) > 0)

  def test_post(self):
    response = self.conn.request_post(self.bucket_url, {'secret_key': 'wrong', 'error': 'an error occurred'}, headers={'Accept': 'application/json'})
    self.assertEqual('401', response['headers']['status'])

    response = self.conn.request_post(self.bucket_url, {'secret_key': self.bucket['secret_key'], 'message': 'an error occurred'}, headers={'Accept': 'application/json'})
    self.assertEqual('200', response['headers']['status'])

if __name__ == '__main__':
  unittest.main()
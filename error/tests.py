from django.test import TestCase
from django.contrib.auth.models import User
from django.db import IntegrityError

from errorbucket.error.models import Bucket, Error

class ErrorTest(TestCase):
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
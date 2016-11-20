# -*- coding: utf-8 -*-

from django.test import TestCase


class ForRentApiTestCase(TestCase):
    def test_home(self):
        response = self.client.get(path='/', )
        self.assertEqual(response.status_code, 200)

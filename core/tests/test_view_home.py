from django.test import TestCase
from django.shortcuts import resolve_url as r

# Create your tests here.
class HomeTest(TestCase):
    def setUp(self):
        self.response = self.client.get(r('home'))

    def test_get(self):
        #GET / must return status code 200
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        #Must use template index.html
        self.assertTemplateUsed(self.response, 'index.html')
    
    def test_subscription_link(self):
        expected = 'href="{}"'.format(r('subscriptions:new'))
        self.assertContains(self.response, expected)

    def test_speakers(self):
        """Must show keynote speakers"""
        contents = [
            'Grace Hopper',
            'hopper.png',
            'Alan Turing',
            'turing.png',
        ]

        for expected in contents:
            with self.subTest():
                self.assertContains(self.response, expected)

    def test_speakers_link(self):
        expected = 'href="{}#speakers"'.format(r('home'))
        self.assertContains(self.response, expected)
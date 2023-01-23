from django.test import TestCase
from core.models import Talk

class TalkModelTest(TestCase):
    def setUp(self):
        self.talk = Talk.objects.create(
            title='Título da Palestra',
            start='10:00',
            description='Descrição da Palestra',
        )
    
    def test_create(self):
        self.assertTrue(Talk.objects.exists())
    
    def test_has_speakers(self):
        """Talk has many Speakers and vice-versa"""
        self.talk.speakers.create(
            name='Tiago Raphael',
            slug='tiago-raphael',
            website='https://www.instagram.com/tiagorafaelamaral/',
        )
        self.assertEqual(1, self.talk.speakers.count())
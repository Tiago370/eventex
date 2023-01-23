from django.test import TestCase
from core.models import Talk

class TalkModelTest():
    def setUp(self):
        self.talk = Talk.objects.create(
            title='Título da Palestra',
            start='10:00',
            description='Descrição da Palestra',
        )
    
    def test_create(self):
        self.assertTrue(Talk.objects.exists())
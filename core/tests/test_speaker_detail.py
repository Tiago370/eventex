
from django.test import TestCase
from core.models import Speaker
from django.shortcuts import resolve_url as r

class SpeakerDetailGet(TestCase):
    def setUp(self):
        Speaker.objects.create(
            name='Tiago Azul',
            description='Programador e pesquisador azul.',
            photo='https://media.licdn.com/dms/image',
            website='http://hbn.link/hopper-site',
            slug='grace-hopper'
        )
        self.response = self.client.get(r('speaker_detail', slug='grace-hopper'))
    
    def test_get(self):
        """GET should return status 200"""
        self.assertEqual(200, self.response.status_code)
    
    def test_template_used(self):
        self.assertTemplateUsed(self.response, 'core/speaker_detail.html')
        
    def test_context(self):
        """Speaker must be in context"""
        speakers = self.response.context['speaker']
        self.assertIsInstance(speakers, Speaker)
    
    def test_speaker(self):
        """Must show keynote speakers"""
        contents = [
            'Tiago Azul',
            'Programador e pesquisador azul.',
            'https://media.licdn.com/dms/image',
            'http://hbn.link/hopper-site',
        ]

        for expected in contents:
            with self.subTest():
                self.assertContains(self.response, expected)
    
class SpeakerDetailNotFound(TestCase):
    def test_not_found(self):
        response = self.client.get(r('speaker_detail', slug='not_found'))
        self.assertEqual(404, response.status_code)
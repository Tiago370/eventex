from django.test import TestCase
from django.shortcuts import resolve_url as r
from core.models import Talk

class TalkListGet(TestCase):
    def setUp(self):
        Talk.objects.create(title='Título da Palestra', start='10:00',
                            description='Descrição da palestra.')
        Talk.objects.create(title='Título da Palestra', start='13:00',
                            description='Descrição da palestra.')


        self.response = self.client.get(r('talk_list'))

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'talk_list.html')
    
    def test_html(self):
        contents = [
            (2, 'Título da Palestra'),
            #(1, '10:00'),
            #(1, '13:00'),
            (2, 'palestrantes/tiago-amaral/'),
            (2, 'Descrição da palestra'),
        ]

        for count, expected in contents:
            with self.subTest():
                self.assertContains(self.response, expected, count)
    
    def test_context(self):
        variables = ['morning_talks', 'afternoon_talks']

        for key in variables:
            with self.subTest():
                self.assertIn(key, self.response.context)
    
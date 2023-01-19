from django.core.exceptions import ValidationError
from django.test import TestCase
from core.models import Speaker, Contact

class ContactModelTest(TestCase):
    def setUp(self):
        self.speaker = Speaker.objects.create(
            name='Tiago Amaral',
            slug='tiago-amaral',
            photo='https://media.licdn.com/dms/image/D4D03AQGeTFHdkv-w_A/profile-displayphoto-shrink_800_800/0/1669686060261?e=2147483647&v=beta&t=D8d-Zz3FK87YuZQ3orcpTMrD112sRT_buV7KqyQDzlQ',
        )

    def test_email(self):
        contact = Contact.objects.create(
            speaker =self.speaker,
            kind = Contact.EMAIL,
            value = 'tiagoamral23@gmail.com',
        )

        self.assertTrue(Contact.objects.exists())
    
    def test_phone(self):
        contact = Contact.objects.create(
            speaker =self.speaker,
            kind = Contact.PHONE,
            value = '011235813',
        )

        self.assertTrue(Contact.objects.exists())

    def test_choice(self):
        """Contact kind should be limited to E or P"""
        contact = Contact.objects.create(
            speaker =self.speaker,
            kind = 'A',
            value = 'B',
        )
        self.assertRaises(ValidationError, contact.full_clean)
    
    def test_str(self):
        contact = Contact(
            speaker =self.speaker,
            kind = Contact.EMAIL,
            value = 'tiagoamral23@gmail.com',
        )
        self.assertEqual('tiagoamral23@gmail.com', str(contact))

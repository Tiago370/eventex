from django.test import TestCase
from subscriptions.models import Subscription
from datetime import datetime

class SubscriptionModelTest(TestCase):
    def setUp(self):
        self.obj = Subscription(
            name='Tiago Rafael',
            cpf='012345778',
            email='tiago.rafael@abc.com.br',
            phone='123567'
        )
        self.obj.save()

    def test_create(self):
        self.assertTrue(Subscription.objects.exists())
    
    def test_crated_at(self):
        #Subscription must an auto created_at attr.
        self.assertIsInstance(self.obj.created_at, datetime)

    def test_str(self):
        self.assertEqual('Tiago Rafael', str(self.obj))
    
    def test_paid_default_to_False(self):
        """By default paid must be False"""
        self.assertEqual(False, self.obj.paid)
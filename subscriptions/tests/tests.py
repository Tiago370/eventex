from django.test import TestCase
from subscriptions.forms import SubscriptionForm
from django.core import mail
from subscriptions.models import Subscription
from django.shortcuts import resolve_url as r

class SubscritpionsNewGet(TestCase):
    def setUp(self):
        self.response = self.client.get(r('subscriptions:new'))

    def test_get(self):
        #Get inscricao/ must return status code 200
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        #Must use subscriptions/subscription_form.html
        self.assertTemplateUsed(self.response, 'subscriptions/subscription_form.html')

    def test_html(self):
        #Html must contain input tags
        self.assertContains(self.response, '<form')
        self.assertContains(self.response, '<input', 6)
        self.assertContains(self.response, 'type="text"', 3)
        self.assertContains(self.response, 'type="email"')
        self.assertContains(self.response, 'type="submit"')


    def test_csrf(self):
        #Html must contain csrf
        self.assertContains(self.response, 'csrfmiddlewaretoken')


    def test_has_form(self):
        #Context must have subscription form
        form = self.response.context['form']
        self.assertIsInstance(form, SubscriptionForm)


    def test_has_fields(self):
        #Form must have 4 fields.
        form = self.response.context["form"]
        self.assertSequenceEqual(['name', 'cpf', 'email', 'phone'], list(form.fields))

    def test_cpf_has_11_digits(self):
        """CPF must only asscept digits."""
        form = self.make_validated_form(cpf='ABCD5678901')
        self.assertFormErrorCode(form, 'cpf', 'digits')

    def test_cpf_has_11_digits(self):
        """CPF must have 11 digits."""
        form = self.make_validated_form(cpf='12345')
        self.assertFormErrorCode(form, 'cpf', 'length')

    def make_validated_form(self, **kwargs):
        valid = dict(
            name='Rafael Henrique da Silva Correia', cpf='12345678901',
            email='rafael@abraseucodigo.com.br', phone='00-90000-9000')
        data = dict(valid, **kwargs)
        form = SubscriptionForm(data)
        form.is_valid()
        return form
    
    def assertFormErrorCode(self, form, field, code):
        errors = form.errors.as_data()
        errors_list = errors[field]
        exception = errors_list[0]
        self.assertEqual(code, exception.code)

class SubscritpionsNewPostValid(TestCase):
    def setUp(self):
        data = dict(name='Tiago Amaral', cpf='09370727612', email='tiago.amaral@kmee.com.br', phone='35 12345690')
        self.response = self.client.post(r('subscriptions:new'), data)

    def test_post(self):
        #Valid POST should redirect to /incricao/1/
        self.assertRedirects(self.response, r('subscriptions:detail', 1))

    def test_send_subscribe_email(self):
        self.assertEqual(1, len(mail.outbox))

    def test_save_subscription(self):
        self.assertTrue(Subscription.objects.exists())
        pass

    def test_subscription_email_subject(self):
        email = mail.outbox[0]
        expect = 'Confirmação de inscrição'
        self.assertEqual(expect, email.subject)

    def test_subscription_email_from(self):
        email = mail.outbox[0]
        expect = 'eventex@email.com'
        self.assertEqual(expect, email.from_email)

    def test_subscription_email_to(self):
        email = mail.outbox[0]
        expect = ['eventex@email.com', 'tiago.amaral@kmee.com.br']
        self.assertEqual(expect, email.to)
    
    def test_subscription_email_body(self):
        email = mail.outbox[0]
        self.assertIn('Tiago Amaral', email.body)
        self.assertIn('09370727612', email.body)
        self.assertIn('tiago.amaral@kmee.com', email.body)
        self.assertIn('35 12345690', email.body)


class SubscritpionsNewPostInvalid(TestCase):
    def setUp(self):
        self.response = self.client.post(r('subscriptions:new'), {})

    def test_post(self):
        #Invalid POST should not redirect
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'subscriptions/subscription_form.html')

    def test_has_form(self):
        form = self.response.context['form']
        self.assertIsInstance(form, SubscriptionForm)
    
    def test_form_has_errors(self):
        form = self.response.context['form']
        self.assertTrue(form.errors)

    def test_dont_save_subscription(self):
        self.assertFalse(Subscription.objects.exists())


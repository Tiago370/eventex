from django.shortcuts import render
from django.conf import settings
from subscriptions.forms import SubscriptionForm
from subscriptions.models import Subscription
from django.http import HttpResponseRedirect, HttpResponse
from django.core import mail
from django.template.loader import render_to_string
from django.contrib import messages

def subscribe(request):
    if request.method == 'POST':
        return create(request)
    else:
        return new(request)

def create(request):
    form = SubscriptionForm(request.POST)
    if not form.is_valid():
        return render(request, 'subscriptions/subscription_form.html', {'form': form})
    
    #Send subscription email
    subscriber_email = form.cleaned_data['email']
    _send_mail(
        'Confirmação de inscrição',
        settings.DEFAULT_FROM_EMAIL,
        subscriber_email,
        'subscriptions/subscription_email.txt',
        form.cleaned_data
    )

    #Success feedback
    messages.success(request, 'Inscrição realizada com sucesso!')
    Subscription.objects.create(**form.cleaned_data)
    return HttpResponseRedirect('/inscricao/')

def new(request):
    context = {'form': SubscriptionForm() }
    return render(request, 'subscriptions/subscription_form.html', context)

def _send_mail(subject, from_, to, template_name, context):
    body = render_to_string(template_name, context)
    mail.send_mail(subject, body, from_, [from_, to])
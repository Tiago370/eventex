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

    subscription = Subscription.objects.create(**form.cleaned_data)
    
    #Send subscription email
    _send_mail(
        'Confirmação de inscrição',
        settings.DEFAULT_FROM_EMAIL,
        subscription.email,
        'subscriptions/subscription_email.txt',
        {'subscription': subscription}
    )
    #Success feedback
    messages.success(request, 'Inscrição realizada com sucesso!')

    return HttpResponseRedirect('/inscricao/{}/'.format(subscription.pk))

def new(request):
    return render(request, 'subscriptions/subscription_form.html', {'form': SubscriptionForm()})

def detail(request, pk):
    subscription = Subscription.objects.get(pk=pk)
    return render(request, 'subscriptions/subscription_detail.html', {'subscription': subscription})

def _send_mail(subject, from_, to, template_name, context):
    body = render_to_string(template_name, context)
    mail.send_mail(subject, body, from_, [from_, to])
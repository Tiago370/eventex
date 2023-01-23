from django.shortcuts import render
from django.views.generic import DetailView
from core.models import Speaker, Talk

# Create your views here.
def home(request):
    return render(request, 'index.html')

def handler404(request, exception):
    return render(request, '404.html')

def talk_list(request):
    context = {
        'morning_talks': Talk.objects.filter(start__lt='12:00'),
        'afternoon_talks': Talk.objects.filter(start__gte='12:00'),
    }
    return render(request, 'talk_list.html', context)

speaker_detail = DetailView.as_view(model=Speaker)
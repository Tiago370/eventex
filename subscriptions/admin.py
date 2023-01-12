from django.contrib import admin
from subscriptions.models import Subscription
from django.utils.timezone import now
# Register your models here.

class SubscriptionModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'cpf', 'created_at', 'subscribed_today')
    date_hierarchy = 'created_at'
    search_fields = ('name', 'email', 'phone', 'cpf', 'created_at')
    list_filter = ('created_at',)

    def subscribed_today(self, obj):
        cd = obj.created_at
        agora = now().date()
        #return obj.created_at == now().date()
        return (cd.year, cd.month, cd.day) == (agora.year, cd.month, cd.day)
    subscribed_today.short_description = 'inscrito hoje?'
    subscribed_today.boolean = True

admin.site.register(Subscription, SubscriptionModelAdmin)
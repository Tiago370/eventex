from django.contrib import admin
from subscriptions.models import Subscription
from django.utils.timezone import now
# Register your models here.

class SubscriptionModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'cpf', 'created_at', 'subscribed_today', 'paid')
    date_hierarchy = 'created_at'
    search_fields = ('name', 'email', 'phone', 'cpf', 'created_at')
    list_filter = ('paid', 'created_at')

    actions = ['mark_as_paid']
    def subscribed_today(self, obj):
        cd = obj.created_at
        agora = now().date()
        #return obj.created_at == now().date()
        return (cd.year, cd.month, cd.day) == (agora.year, agora.month, agora.day)
    subscribed_today.short_description = 'inscrito hoje?'
    subscribed_today.boolean = True

    def mark_as_paid(self, request, queryset):
        count = queryset.update(paid = True)
        if count == 1:
            msg = '{} inscrição foi marcada como paga.'
        else:
            msg = '{} inscrições foram marcadas como pagas.'
        self.message_user(request, msg.format(count))
    mark_as_paid.short_description = 'Marcar como pago'

admin.site.register(Subscription, SubscriptionModelAdmin)
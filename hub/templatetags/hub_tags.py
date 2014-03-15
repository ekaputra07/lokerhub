from django import template
from django.core.urlresolvers import reverse
register = template.Library()

from hub.models import PaymentConfirmation, PremiumOrder


@register.filter(name='addclass')
def addclass(field, css):
   return field.as_widget(attrs={"class":css})


@register.filter(name='nospam')
def nospam(email):
    return email.replace('@', ' [at] ')


@register.filter(name='admin_order_url_from_confirm_id')
def admin_order_url_from_confirm_id(confirm_id):
    try:
        confirm = PaymentConfirmation.objects.get(pk=confirm_id)
    except:
        return '#'
    else:
        return reverse('admin:hub_premiumorder_change', args=[confirm.order.pk])


@register.simple_tag(name='unpaid_bills', takes_context=True)
def unpaid_bill(context, var):
    user = context.get('user')
    order = PremiumOrder.objects.filter(user=user, status='UNPAID')
    context[var] = len(order)
    return ''



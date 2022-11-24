from django import template
from mainApp.models import Checkout, CheckoutProducts
register = template.Library()


@register.filter(name='checkoutProducts')
def checkoutProducts(checkoutid):
    checkout = Checkout.objects.get(id=checkoutid)
    cp = CheckoutProducts.objects.filter(checkout=checkout)
    return cp


@register.filter(name='paymentMode')
def paymentMode(m):
    if m == 0:
        print(m, "\n\n\n")
        return "COD"
    elif m == 1:
        return "Net Banking"


@register.filter(name='paymentStatus')
def paymentStatus(op):
    if op == 0:
        return "Pending"
    elif op == 1:
        return "Done"

@register.filter(name='orderStatus')
def orderStatus(op):
    if op == 0:
        return "Order Placed"
    elif op == 1:
        return "Not Packed"
    elif op == 2:
        return "Packed"
    elif op == 3:
        return "Ready to Ship"
    elif op == 4:
        return "Shipped"
    elif op == 5:
        return "Out for Delivery"
    elif op == 6:
        return "Delivered"
    elif op == 7:
        return "Cancelled"

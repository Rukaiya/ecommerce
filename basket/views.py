from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .basket import Basket

from store.models import Product


def basket_summary(request):
    basket = Basket(request)
    return render(request, 'store/basket/summary.html', { 'basket': basket })


def basket_add(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        product = get_object_or_404(Product, id=product_id)
        basket.add(product=product, quantity=product_qty)
        basket_qty = basket.__len__()
        response = JsonResponse({'quantity': basket_qty})
        return response

def basket_delete(request):
    basket = Basket(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        basket.delete(product_id=product_id)

        basketqty = basket.__len__()
        baskettotal = basket.get_total_price()
        response = JsonResponse({'quantity': basketqty, 'subtotal': baskettotal})
        return response

def basket_update(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        basket.update(product_id=product_id, quantity=product_qty)

        basketqty = basket.__len__()
        baskettotal = basket.get_total_price()
        response = JsonResponse({'quantity': basketqty, 'subtotal': baskettotal})
        return response

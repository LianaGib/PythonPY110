from django.shortcuts import render
from django.contrib.auth import get_user
from logic.services import view_in_wishlist
from store.models import DATABASE
from django.http import JsonResponse


# Create your views here.
def wishlist_view(request):
    if request.method == "GET":
        current_user = get_user(request).username
        data = view_in_wishlist(request)[current_user]  # TODO получить продукты из избранного для пользователя
        if request.GET.get('format') == 'JSON':
            return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
                                                         'indent': 4})
        products = []
        # TODO сформировать список словарей продуктов с их характеристиками
        for product_id, quantity in data.items():
            product = DATABASE[
                product_id]
            product[
                'quantity'] = quantity
            product[
                "price_total"] = f"{quantity * product['price_after']:.2f}"
            products.append(product)
        return render(request, 'wishlist/wishlist.html', context={"products": products})


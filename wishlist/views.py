from django.shortcuts import render, redirect
from django.contrib.auth import get_user
from logic.services import view_in_wishlist, add_to_wishlist, remove_from_wishlist
from store.models import DATABASE
from django.http import JsonResponse, HttpResponseNotFound
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='login:login_view')
def wishlist_view(request):
    if request.method == "GET":
        current_user = get_user(request).username
        data = view_in_wishlist(request)[current_user]  # TODO получить продукты из избранного для пользователя
        if request.GET.get('format') == 'JSON':
            return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
                                                         'indent': 4})
        products = []
        # TODO сформировать список словарей продуктов с их характеристиками
        for product_id in data["products"]:
            products.append(DATABASE[product_id])
        return render(request, 'wishlist/wishlist.html', context={"products": products})


def wishlist_remove_view(request, id_product):
    if request.method == "GET":
        result = remove_from_wishlist(request, id_product)  # TODO Вызвать функцию удаления из корзины
        if result:
            return redirect("wishlist:wishlist_view")  # TODO Вернуть перенаправление на корзину

        return HttpResponseNotFound("Неудачное удаление из корзины")


@login_required(login_url='login:login_view')
def wishlist_add_json(request, id_product: str):
    """
    Добавление продукта в избранное и возвращение информации об успехе или неудаче в JSON
    """
    if request.method == "GET":
        result = add_to_wishlist(request, id_product)
        if result:
            return JsonResponse({"answer": "Продукт успешно добавлен в избранное"},
                                json_dumps_params={'ensure_ascii': False})

        return JsonResponse({"answer": "Неудачное добавление в избранное"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})


def wishlist_del_json(request, id_product: str):
    """
    Удаление продукта из избранного и возвращение информации об успехе или неудаче в JSON
    """
    if request.method == "GET":
        result = remove_from_wishlist(request, id_product)  # TODO вызовите обработчик из services.py удаляющий продукт из избранного
        if result:
            return JsonResponse({"answer": "Продукт успешно удалён из избранного"},
                                json_dumps_params={'ensure_ascii': False})

        return JsonResponse({"answer": "Неудачное удаление из избранного"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})


def wishlist_json(request):
    """
    Просмотр всех продуктов в избранном для пользователя и возвращение этого в JSON
    """
    if request.method == "GET":
        current_user = get_user(request).username  # from django.contrib.auth import get_user
        data = view_in_wishlist(current_user)  # TODO получите данные о списке товаров в избранном у пользователя
        if data:
            return JsonResponse(data, json_dumps_params={'ensure_ascii': False})  # TODO верните JsonResponse c data

        return JsonResponse({"answer": "Неудачное удаление из избранного"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})  # TODO верните JsonResponse с ключом "answer" и значением "Пользователь не авторизирован" и параметром status=404

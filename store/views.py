from django.shortcuts import render
from django.http import JsonResponse
from .models import DATABASE
from django.http import HttpResponse, HttpResponseNotFound

def shop_view(request):
    if request.method == "GET":
        with open('store/shop.html', encoding="utf-8") as f:
            data = f.read()
        return HttpResponse(data)

def products_view(request):
    if request.method == "GET":
        id = request.GET.get('id')
        if id in DATABASE:
            return JsonResponse(DATABASE[id], json_dumps_params={'ensure_ascii': False,
                                                             'indent': 4})
        if id not in DATABASE:
            return HttpResponseNotFound("Данного продукта нет в базе данных")
    if request.method is None:
        return JsonResponse(DATABASE, json_dumps_params={'ensure_ascii': False,
                                                         'indent': 4})
# Create your views here.
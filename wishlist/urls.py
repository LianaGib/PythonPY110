from django.urls import path
from .views import wishlist_view, wishlist_remove_view, wishlist_add_json, wishlist_del_json, wishlist_json

#  TODO Импортируйте ваше представление

app_name = 'wishlist'

urlpatterns = [
    path('', wishlist_view, name="wishlist_view"),  # TODO Зарегистрируйте обработчик
    path('delete/<int:id_product>', wishlist_remove_view, name="wishlist_remove_view"),
    path('api/add/<id_product>', wishlist_add_json, name="wishlist_add_json"),
    path('api/del/<id_product>', wishlist_del_json, name="wishlist_del_json"),
    path('api/', wishlist_json, name="wishlist_json"),
]
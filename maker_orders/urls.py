from django.contrib import admin
from django.urls import path
from maker_orders.views import home_page_view, OrderDetailView, make_order_view
    # , HomePageView

urlpatterns = [
    path('test/', home_page_view),
    # path('new_user', UserCreateView)
    path('orders/<user_id>/', make_order_view, name='orders_list_url'),
    path('make_order/<id_>/', OrderDetailView.as_view(), name='order_detail_url')

]

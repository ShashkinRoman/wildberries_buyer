from django.shortcuts import render
from django.views import View
from django.shortcuts import get_object_or_404
# from maker_orders.forms import UserForm
from maker_orders.models import Order
from maker_orders.servises import ObjectDetailMixin
# Create your views here.


# class UserCreateView(View):
#     def get(self, request):
#         # form = UserForm()
#         form = 'test'
#         return render(request,  'maker_orders/user_create.html', context={'form': form})


def home_page_view(request):
    # def get(self, request):
    return render(request, 'maker_orders/base_block.html')


def make_order_view(request, user_id):
    ordered = Order.objects.filter(owner_id=user_id)
    return render(request, 'maker_orders/make_order.html', context={'order': ordered})


# class OrderView(View):
#
#     def get(self, request, user_id):
#         ordered = Order.objects.filter(owner=user_id)
#         return render(request, 'maker_orders/make_order.html', context={'order': ordered})


class OrderDetailView(ObjectDetailMixin, View):
    model = Order
    template = 'maker_orders/order_detail.html'

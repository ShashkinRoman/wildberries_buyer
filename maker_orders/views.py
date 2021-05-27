# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render, redirect
# from django.views import View
# from django.shortcuts import get_object_or_404
# pipfrom maker_orders.forms import OrderForm, LikeCreateForm
#     # UserCreateForm,\
#
# from maker_orders.models import Order
# from maker_orders.servises import ObjectDetailMixin
# # Create your views here.
#
#
# # class UserCreateView(View):
# #     def get(self, request):
# #         form = UserCreateForm()
# #         return render(request,  'maker_orders/user_create.html', context={'form': form})
# #
# #     def post(self, request):
# #         bound_form = UserCreateForm(request.POST)
# #
# #         if bound_form.is_valid():
# #             bound_form.save()
# #             return redirect('home_page')
# #
# #         return render(request, 'maker_orders/user_create.html', context={'form': bound_form})
#
#
# class LikesCreateView(View):
#     def get(self, request):
#         form = LikeCreateForm()
#         # return
#         pass
#
#
# @login_required
# def home_page_view(request):
#     # def get(self, request):
#     return render(request, 'maker_orders/base_block.html')
#
#
# def orders_view(request, user_id):
#     ordered = Order.objects.filter(owner_id=user_id)
#     return render(request, 'maker_orders/make_order.html', context={'order': ordered})
#
#
# # class OrderView(View):
# #
# #     def get(self, request, user_id):
# #         ordered = Order.objects.filter(owner=user_id)
# #         return render(request, 'maker_orders/make_order.html', context={'order': ordered})
#
#
# class OrderDetailView(ObjectDetailMixin, View):
#     model = Order
#     template = 'maker_orders/order_detail.html'
#
#
# class OrderCreateView(View):
#     def get(self, request, user_id):
#         form = OrderForm()
#
#         return render(request, 'maker_orders/order_create.html', context={'form': form})
#     # def post(self request()):
#
#
#

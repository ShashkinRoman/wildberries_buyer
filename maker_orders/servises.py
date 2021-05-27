# from django.shortcuts import render
# from django.shortcuts import get_object_or_404
#
# from maker_orders.models import Order
#
#
# class ObjectDetailMixin:
#     model = None
#     template = None
#
#     def get(self, request, id_):
#         obj = get_object_or_404(self.model, id=id_)
#         return render(request, self.template, context={self.model.__name__.lower(): obj})


def create_order():
    """
    check free number,
    if have_not number take number from sms-activate
    authorization
    take sms, decode captcha
    make_orders
    :return:
    """


def add_to_cart():
    """
    find several random products, and add to cart by product_id
    :return:
    """


def put_like_the_product():
    """
    put like posts, by search requests, and browses several random products
    folow in brand page and put like
    :return:
    """


def put_like_the_brand():
    """
    put like brand, find product by search requests, browses several random products

    :return:
    """


def ask_questions():
    """
    by product id find by search requests, browses several random products,go on product page ans asl question
    :return:
    """



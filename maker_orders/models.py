from django.db import models
from datetime import datetime
from django.shortcuts import reverse
from django.contrib.auth.models import User
# Create your models here.


# class UserModel(User):
#     """Owner, who will be make orders"""
#     phone_number = models.CharField(max_length=11, blank=True, unique=True)


class SearchRequest(models.Model):
    """Requests for which will be all activity with products by several phone number"""
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rn_user_inside_search_request')
    # todo узнать почему можно записать только id, а не инстанс класса Producr
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='rn_product_inside_search_request')
    request = models.CharField(max_length=255)


class Product(models.Model):
    """Product for which will be all activity"""
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rn_user_inside_product')
    id_product = models.CharField(max_length=255)
    search_requests = models.ManyToManyField(SearchRequest, related_name='rn_search_request_inside_product')


class ActionWithProduct(models.Model):
    """All activity for products"""
    LIKE = 'lk'
    FAVORITES = 'fv'
    BRAND_FAVORITES = 'bfv'
    ORDER = 'or'
    QUESTIONS = 'qs'
    REVIEW = 'rv'
    ACTION_WITH_PRODUCTS_CHOICES = [
        (LIKE, 'like'),
        (FAVORITES, 'favorites'),
        (BRAND_FAVORITES, 'brand_favorites'),
        (ORDER, 'order'),
        (QUESTIONS, 'questions'),
        (REVIEW, 'review'),
    ]

    phone_number = models.ForeignKey('Phone', on_delete=models.CASCADE,
                                     related_name='rn_phone_inside_action_with_product')
    product = models.ForeignKey(
        'Product', on_delete=models.CASCADE, related_name='rn_product_inside_action_with_product')
    action_type = models.CharField(max_length=5, choices=ACTION_WITH_PRODUCTS_CHOICES, blank=True)
    created_at = models.DateTimeField(default=datetime.now())
    search_request = models.ForeignKey('SearchRequest', on_delete=models.CASCADE,
                                       related_name='rn_search_request_action_with_product', default='')


class Phone(models.Model):
    """Phones from sms-activate with dates and activity"""
    ONE_SMS = 'sms'
    RENT = 'rent'
    DEACTIVATE = 'dc'
    STATUS_RENT_CHOICES = [
        (ONE_SMS, 'one_sms_rent'),
        (RENT, 'daily_rent'),
        (DEACTIVATE, 'deactivate')
    ]
    id_rent = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=11, unique=True)
    start_rent_date = models.DateTimeField(default=datetime.now())
    end_rent_date = models.DateTimeField(blank=True)
    status_rent = models.CharField(max_length=5, choices=STATUS_RENT_CHOICES, blank=True)
    # actions = models.ManyToManyField(ActionWithProduct)


# todo change fields city, region, addresses on foreignkey
class Order(models.Model):
    """Save all order information and qr for payment in base64"""
    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name='rn_user_inside_order', null=True)
    id_product = models.ForeignKey('Product', on_delete=models.CASCADE,
                                   related_name='rn_products_inside_order')
    region = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    house = models.CharField(max_length=255)
    phone_number = models.ForeignKey('Phone', on_delete=models.CASCADE,
                                     related_name='orders')
    # quantity = models.SmallIntegerField()
    search_request = models.ForeignKey('SearchRequest', on_delete=models.CASCADE,
                                       related_name='orders')
    size = models.CharField(max_length=255)
    delivery_method = models.CharField(max_length=255)
    flat = models.CharField(max_length=255, blank=True)
    private_house = models.BooleanField(default=False, blank=True)
    # date_buyout = models.DateTimeField(blank=True)
    created_at = models.DateTimeField(blank=True)
    qr = models.CharField(max_length=150000, blank=True)
    SUCCESS = 'sc'
    ORDERED = 'or'
    DELIVERY = 'dl'
    DELIVERED = 'dld'

    ORDER_STATUS_CHOICES = [
        (SUCCESS, 'success'),
        (ORDERED, 'ordered'),
        (DELIVERY, 'delivery'),
        (DELIVERED, 'delivered')
    ]

    order_status = models.CharField(max_length=5, choices=ORDER_STATUS_CHOICES, blank=True)

    def get_absolute_url(self):
        return reverse('order_detail_url', kwargs={'user_id': self.id})

    def __str__(self):
        return f'{self.id_product} {self.region} {self.city} {self.search_request}'


class ReviewAndQuestions(models.Model):
    action_id = models.ForeignKey('ActionWithProduct', on_delete=models.CASCADE,
                                  related_name='rn_action_with_product_inside_review')
    review_text = models.CharField(max_length=2000)
# class Brand(models.Model):
#     name = models.CharField(max_length=255)
#     url = models.CharField(max_length=3000)

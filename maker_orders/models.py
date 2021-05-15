from django.db import models
from datetime import datetime
# Create your models here.


class User(models.Model):
    """Owner, who will be make orders"""
    first_name = models.CharField(max_length=255, blank=True)
    second_name = models.CharField(max_length=255, blank=True)
    mail = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=11, blank=True)


class Search_request(models.Model):
    """Requests for which will be all activity with products by several phone number"""
    user_id = models.ForeignKey('User', on_delete=models.CASCADE, related_name='rn_user_inside_search_request')
    # todo узнать почему можно записать только id, а не инстанс класса Producr
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='rn_product_inside_search_request')
    request = models.CharField(max_length=255)


class Product(models.Model):
    """Product for which will be all activity"""
    user_id = models.ForeignKey('User', on_delete=models.CASCADE, related_name='rn_user_inside_product')
    id_product = models.CharField(max_length=255)
    search_requests = models.ManyToManyField(Search_request, related_name='rn_search_request_inside_product')


class ActionWithProduct(models.Model):
    """All activity for products"""
    LIKE = 'lk'
    FAVORITES = 'fv'
    BRAND_FAVORITES = 'bfv'
    ORDER = 'or'
    QUESTIONS = 'qw'
    REVIEW = 're'
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
    search_request = models.ForeignKey('Search_request', on_delete=models.CASCADE,
                                     related_name='rn_search_request_action_with_product', default='')


class Phone(models.Model):
    """Phones from sms-activate with dates and activity"""
    phone_number = models.CharField(max_length=11, unique=True)
    start_rent_date = models.DateTimeField(default=datetime.now())
    end_rent_date = models.DateTimeField(blank=True, unique=True)
    actions = models.ManyToManyField(ActionWithProduct)


# todo change fields city, region, addresses on foreignkey
class Order(models.Model):
    """Save all order information and qr for payment in base64"""
    owner = models.ForeignKey('User', on_delete=models.CASCADE,
                              related_name='rn_user_inside_order', null=True)
    id_product = models.ForeignKey('Product', on_delete=models.CASCADE,
                                   related_name='rn_products_inside_order')
    region = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    house = models.CharField(max_length=255)
    phone_number = models.ForeignKey('Phone', on_delete=models.CASCADE,
                                     related_name='rn_phone_inside_order')
    # quantity = models.SmallIntegerField()
    search_request = models.ForeignKey('Search_request', on_delete=models.CASCADE,
                                       related_name='rn_search_request_inside_order')
    size = models.CharField(max_length=255)
    delivery_method = models.CharField(max_length=255)
    flat = models.CharField(max_length=255)
    private_house = models.BooleanField(default=False)
    # date_buyout = models.DateTimeField(blank=True)
    created_at = models.DateTimeField(blank=True)
    qr = models.CharField(max_length=150000, blank=True)

    def __str__(self):
        return f'{self.id_product} {self.region} {self.city} {self.search_request}'

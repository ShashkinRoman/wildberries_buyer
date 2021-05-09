from django.db import models
from datetime import datetime
# Create your models here.


# todo change fields city, region, addresses on foreignkey
class Order(models.Model):
    id_product = models.IntegerField()
    region = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    house = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    # quantity = models.SmallIntegerField()
    search_request = models.CharField(max_length=255)
    # product_id = models.CharField(max_length=255)
    size = models.CharField(max_length=255)
    delivery_method = models.CharField(max_length=255)
    flat = models.CharField(max_length=255)
    private_house = models.BooleanField(default=False)
    # date_buyout = models.DateTimeField(blank=True)
    created_at = models.DateTimeField(blank=True)
    qr = models.CharField(max_length=150000, blank=True)

    def __str__(self):
        return f'{self.id_product} {self.region} {self.city} {self.search_request}'


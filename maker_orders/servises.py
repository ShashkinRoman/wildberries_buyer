from maker_orders.models import ActionWithProduct, Order
from maker_orders.utils import look_random_products, find_by_request, registration, find_phone, go_on_product_page, \
    ad_to_cart, Chromedriver, put_like_the_product_on_page, add_brand_favorites, make_order, qr_saver
from wildberries_buyer.settings import BASE_DIR as bd
from random import uniform
from time import sleep
from datetime import datetime


def driver_start():
    driver_obj = Chromedriver()
    driver = driver_obj.start_driver(str(bd) + '/chromedriver')
    return driver


def add_to_cart(driver, product_id, size, search_request):
    """
    find several random products, add to cart by product_id and write in ActionWithProduct
    :return:
    """
    try:
        phone = find_phone(product_id.id_product, 'atc')
        registration(driver, phone)
        find_by_request(driver, search_request.request)
        look_random_products(driver)
        go_on_product_page(driver, product_id.id_product)
        ad_to_cart(driver, size)
        action_ad_to_cart = ActionWithProduct.objects.create(action_type='atc',
                                                           phone_number_id=phone.id,
                                                           product_id=product_id.id,
                                                           search_request=search_request)

        phone.rn_phone_inside_action_with_product.add(action_ad_to_cart)
    except Exception as e:
        print(e)


def put_like_the_product(driver, product_id, search_request):
    """
    put like posts, by search requests, and browses several random products
    folow in brand page and put like
    :param driver: instance driver
    :param product_id: instance Product
    :param search_request: instance SearchRequest
    :return:
    """
    phone = find_phone(product_id, 'lk')
    registration(driver, phone.phone_number)
    sleep(uniform(1.15, 1.51))
    find_by_request(driver, search_request.request)
    look_random_products(driver)
    go_on_product_page(driver, product_id.id_product)
    put_like_the_product_on_page(driver)
    action_question = ActionWithProduct.objects.create(action_type='lk',
                                                       phone_number_id=phone.id,
                                                       product_id=product_id.id,
                                                       search_request=search_request)
    phone.rn_phone_inside_action_with_product.add(action_question)


def put_like_the_brand(driver, product_id, search_request):
    """
    put like brand, find product by search requests, browses several random product
    """
    phone = find_phone(product_id.id_product, 'bfv')
    registration(driver, phone.phone_number)
    find_by_request(driver, search_request.request)
    look_random_products(driver)
    go_on_product_page(driver, product_id.id_product)

    add_brand_favorites(driver)

    action_add_brand_favorites = ActionWithProduct.objects.create(action_type='bfv',
                                                       phone_number_id=phone.id,
                                                       product_id=product_id.id,
                                                       search_request=search_request)
    phone.rn_phone_inside_action_with_product.add(action_add_brand_favorites)


def ask_questions(driver, product_id, search_request, question):
    """
    by product id find by search requests, browses several random products,go on product page ans asl question
    :return:
    """
    phone = find_phone(product_id.id_product, 'qs')
    registration(driver, phone.phone_number)
    find_by_request(driver, search_request.request)
    look_random_products(driver)
    go_on_product_page(driver, product_id.id_product)

    ask_questions(driver, question)

    action_question = ActionWithProduct.objects.create(action_type='qw',
                                                           phone_number_id=phone,
                                                           product_id=product_id,
                                                           search_request=search_request)

    phone.rn_phone_inside_action_with_product.add(action_question)


def create_order(driver, addresses: tuple, product_id, size: str,
               delivery_method:str, flat: str, private_house: bool, name: tuple,
               search_request, phone):
    """
    check free number,
    if have_not number take number from sms-activate
    authorization
    take sms, decode captcha
    make_orders
    :return:
    """

    phone = find_phone(product_id.id_product, 'or')
    registration(driver, phone.phone_number)
    find_by_request(driver, search_request.request)
    look_random_products(driver)
    go_on_product_page(driver, product_id.id_product)
    ad_to_cart(driver, size)
    make_order(driver, addresses, product_id,
    delivery_method, flat, private_house, name,
    search_request, phone)

    qr = qr_saver(driver)
    Order.objects.create(id_product=product_id, region=addresses[0], city=addresses[1], street=addresses[2],
                         house=addresses[3], phone_number=phone, search_request=search_request,
                         size=size, delivery_method=delivery_method,
                         flat=flat, private_house=private_house, created_at=datetime.now(), qr=qr)

    action_order = ActionWithProduct.objects.create(action_type='or',
                                                       phone_number_id=phone.id,
                                                       product_id=product_id.id,
                                                       search_request=search_request)
    phone.rn_phone_inside_action_with_product.add(action_order)

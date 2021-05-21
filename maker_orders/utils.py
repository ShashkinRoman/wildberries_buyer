from random import uniform, randrange, randint
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from dotenv import load_dotenv
from time import sleep
from selenium.webdriver.common.keys import Keys
from wildberries_buyer.settings import BASE_DIR as bd
from PIL import Image
import base64
from io import BytesIO
from datetime import datetime, date, timedelta
from maker_orders.models import Search_request, Phone, ActionWithProduct, Product, Order, User
load_dotenv()


class Chromedriver():
    def start_driver(self, webdriver_path,
                     # chrome_profile=str(bd) + os.getenv('chrome_profile_one')
                     ):
        options = Options()
        # prefs = {"profile.managed_default_content_settings.images": 2}
        options.binary_location = '/opt/google/chrome/google-chrome'
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36")
        # options.add_experimental_option("prefs", pfrom selenium.webdriver.common.action_chains import ActionChainsrefs)
        options.add_argument("--window-size=1050,853")
        # options.add_argument('--headless')
        # options.add_argument('--no-sandbox')
        # options.add_argument("load-extension=" + path_extension)
        options.add_argument('--user-data-dir=' + webdriver_path)
        self.driver = webdriver.Chrome(executable_path=webdriver_path,
                                       # options=options
                                       )
        return self.driver


def registration(driver, phone_number: str):
    """
    :param driver: open session selenium webdriver
    :param phone_number: 79371234567
    :return: authorization in wildberries inside driver session
    """
    sleep(uniform(3.15, 5.51))

    driver.get('https://www.wildberries.ru/')
    driver.find_elements_by_class_name('navbar-pc__item')[1].click()
    sleep(0.5)
    for number in phone_number:
        driver.find_elements_by_class_name('input-item')[0].send_keys(f'{number}')
        sleep(uniform(0.15, 1.51))
    sleep(0.5)
    button_get_code = driver.find_elements_by_class_name('i-form-block-v1')
    button_get_code[-1].click()
    captcha_image = driver.find_element_by_class_name('captcha-image').get_attribute('src')
    # captcha_text = captcha(captcha_image)
    # driver.find_element_by_class_name('captcha-input').send_keys(captcha_text)
    button_next = driver.find_elements_by_class_name('i-form-block-v1')
    button_next[1].click()
    print("введите номер")
    field_code = driver.find_elements_by_class_name('input-item')
    # field_code[1].send_keys(code_registration(phone_number))


# todo add sms-activate
# def take_free_number():
#     """
#     return free number from sms-activate
#     :return: 9271234567
#     """
#     return ''


# todo add recaptcha decoding
# def captcha(captcha_image):
#     """
#     return free number from sms-activate
#     :return: str(ExAmPlE)"""
#     print("Input captcha wait 20 sec")
#     sleep(20)
    # return ''


# todo add sms-activate
# def code_registration(phone):
#     """
#     request sms code for phone number from sms-activate
#     :param phone: 9271234567
#     :return: str(123654)
#     """
#     pass


def look_random_products(driver):
    """
    click on random 2-4 products on page scrolling page, ant returned to original page
    :param driver: selenium webdriver instance with open page
    """
    url = driver.current_url
    action = ActionChains(driver)
    for product in range(0, randint(1,2)):
        try:
            find_products = driver.find_elements_by_class_name('ref_goods_n_p')
            sleep(randrange(5))
            selected_product = find_products[randrange(len(find_products))]
            driver.execute_script("arguments[0].scrollIntoView();", selected_product)
            sleep(uniform(1.15, 4.51))
            selected_product.click()
            sleep(uniform(1.15, 4.51))
            scroll_range = 600
            for i in range(10, 15):
                driver.execute_script(f"window.scrollTo(0, {scroll_range})")
                scroll_range += randint(500, 1000)
                sleep(uniform(1.15, 2.51))
            driver.get(url)
            sleep(2)
        except Exception as e:
            print(e)
            driver.get(url)


def find_by_request(driver, search_request: str):
    """
    imitate input search request
    :param search_request: ремень
    :param driver: authorized session selenium
    """
    driver.get('https://www.wildberries.ru/')
    sleep(uniform(0.93, 5.44))
    search_field = driver.find_element_by_class_name('search-catalog__input')
    for letter in search_request:
        search_field.send_keys(letter)
        sleep(uniform(0.15, 1.51))
    search_field.send_keys(Keys.RETURN)


def go_on_product_page(driver, product_id: str):
    """
    click in search field and enter search request
    :param driver:  instance webdriver with open home or catalog page
    :param product_id: str(17503787)
    :return:
    """
    counter = 0
    i = 0
    while i == 0:
        sleep(0.76)
        all_products = driver.find_elements_by_class_name('i-dtList')
        for product in all_products:
            if product.get_attribute('data-catalogercod1s') == product_id:
                product.click()
                sleep(1)
                i = 1
                break
        if i == 1:
            break

        sleep(0.5)
        pages = driver.find_elements_by_class_name('pagination-next')
        driver.execute_script(f"window.scrollTo(0, 2500)")
        sleep(0.5)
        driver.execute_script("arguments[0].click();", pages[0])
        counter += 1
        if counter >= 3:
            i = 1
            print(f'product_id {product_id}, nor found')


def select_addresses(driver, delivery_method: str, addresses: tuple, flat: str, private_house: bool):
    """
    select addresses in product basket
    :param driver: instance webdriver with open order purchase
    :param delivery_method: 'courier' or 'point'
    :param addresses: 'г Балаково, Саратовское Шоссе 39'
    :param flat: '123'
    :param private_house: True
    """
    # check old addresses and delete, if find
    addresses = ' '.join(addresses)
    try:
        driver.find_element_by_class_name('history__menu').click()
        sleep(uniform(.15, .51))
        driver.find_element_by_class_name('address-delete').click()
    except:
        print("can't delete addressee")

    if delivery_method == 'poin':
        select_delivery_method = driver.find_elements_by_class_name('c-radio-withText')
        select_delivery_method[0].click()
        sleep(uniform(.15, .51))

        button_select_addresses = driver.find_elements_by_class_name('c-btn-base-sm')
        button_select_addresses[0].click()
        sleep(uniform(2.15, 3.51))

        input_addresses = driver.find_element_by_class_name('ymaps-2-1-78-searchbox-input__input')
        for litter in addresses:
            input_addresses.send_keys(litter)
            sleep(uniform(.15, .51))
        # select_addresses.send_keys(addresses)
        input_addresses.send_keys(Keys.RETURN)
        sleep(uniform(.15, 1.51))

        select_addresses = driver.find_element_by_class_name('overview').find_elements_by_tag_name('li')
        select_addresses[0].click()
        sleep(uniform(.15, 1.51))

        submit_addresses = driver.find_element_by_class_name('balloon-content-block')
        submit_addresses.find_elements_by_tag_name('button')[0].click()

    if delivery_method == 'courier':
        driver.find_element_by_class_name('t-courier').click()

        sleep(uniform(.15, .51))

        button_select_addresses = driver.find_elements_by_class_name('c-btn-base-sm')
        button_select_addresses[-1].click()
        sleep(uniform(2.15, 3.51))

        input_addresses = driver.find_elements_by_class_name('ymaps-2-1-78-searchbox-input__input')
        for litter in addresses:
            input_addresses[-1].send_keys(litter)
            sleep(uniform(.15, .51))
        input_addresses[-1].send_keys(Keys.RETURN)

        sleep(3)
        add_detail_info = driver.find_elements_by_class_name('added-addres-half')
        for i in flat:
            add_detail_info[-1].send_keys(i)
            sleep(uniform(.15, .51))

        sleep(0.5)
        if private_house:
            checkout = driver.find_elements_by_class_name('c-checkbox-withText')
            checkout[1].click()

        submit_addresses = driver.find_element_by_class_name('added-addres-save')
        submit_addresses.click()


def make_order(driver, addresses: tuple, product_id, size: str,
               delivery_method:str, flat: str, private_house: bool, name: tuple,
               search_request):
    """
    adding product to cart and purchase order
    :param driver: instance webdriver with open product page
    :param addresses:
    :param product_id: instance Product
    :param size:
    :param delivery_method:
    :return:
    """
    try:
        phone = find_phone(product_id.id_product, 'or')
        go_on_product_page(driver, product_id.id_product)
        driver.execute_script(f"window.scrollTo(0, {randint(300, 600)})")

        try:
            sizes = driver.find_elements_by_class_name('j-size')
            select_size = [i.find_element_by_tag_name('span') for i in sizes if size == i.find_element_by_tag_name('span').text]
            select_size[0].click()
        except:
            print("cant't select size")

        add_to_cart = driver.find_elements_by_class_name('c-btn-main-lg-v1')
        add_to_cart[0].click()
        sleep(uniform(0.15, 1.51))

        sleep(uniform(2.15, 3.51))
        go_to_cart = driver.find_elements_by_class_name('navbar-pc__icon--basket')
        go_to_cart[0].click()
        sleep(uniform(2.15, 3.51))

        sleep(uniform(01.15, 1.51))
        go_to_ordering = driver.find_elements_by_class_name('j-item-basket')
        go_to_ordering[0].click()

        sleep(1)
        select_addresses(driver, delivery_method, addresses, flat, private_house)

        sleep(0.5)
        try:
            qr_code_button = driver.find_elements_by_class_name('basket-label')
            qr_code_button[-1].click()
        except:
            print('qr code already selected')

        try:
            sleep(uniform(01.15, 1.51))
            field_input = driver.find_elements_by_class_name('wrap-input')
            first_name_input = field_input[0].find_elements_by_class_name('c-input-base')[0]
            driver.execute_script("arguments[0].scrollIntoView();", first_name_input)
            first_name_input.send_keys(name[0])
            sleep(uniform(01.15, 1.51))
            second_name_input = field_input[1].find_elements_by_class_name('c-input-base')[0]
            second_name_input.send_keys(name[1])
            sleep(uniform(01.15, 1.51))


        except Exception as e:
            print(e)

        sleep(uniform(1.15, 1.51))
        order_accept = driver.find_element_by_class_name('c-btn-main-lg')
        driver.execute_script("arguments[0].scrollIntoView();", order_accept)
        sleep(0.5)
        order_accept.click()

        sleep(uniform(1.15, 1.51))
        driver.find_element_by_class_name('alert-popup-close').click()

        sleep(uniform(1.15, 1.51))

        qr = qr_saver(driver)

        Order.objects.create(id_product=product_id, region=addresses[0], city=addresses[1], street=addresses[2],
                             house=addresses[3], phone_number=phone, search_request=search_request,
                             size=size, delivery_method=delivery_method,
                             flat=flat, private_house=private_house, created_at=datetime.now(), qr=qr)

        action_question = ActionWithProduct.objects.create(action_type='or',
                                                           phone_number_id=phone.id,
                                                           product_id=product_id.id,
                                                           search_request=search_request)
        phone.rn_phone_inside_action_with_product.add(action_question)

    except Exception as e:
        print(e, f'cant make order for product id {product_id.id_product}')


def qr_saver(driver):
    """
    :param driver:
    :return:
    """
    # take screenshot
    driver.save_screenshot("pageImage.jpeg")

    # crop image
    im = Image.open('pageImage.jpeg')
    qr_image = im.crop((int(780), int(640), int(1275), int(1130)))
    # qr_image.save('qr_example.png')

    rgb_qr = qr_image.convert('RGB')
    im_file = BytesIO()
    rgb_qr.save(im_file, format="JPEG")
    im_bytes = im_file.getvalue()  # im_bytes: image in binary format.
    qr_b64 = base64.b64encode(im_bytes)
    return qr_b64


def put_like_the_product(driver, search_request, product_id):
    """
    put like posts, by search requests, and browses several random products
    :param driver: instance selenium webdriver logout wildberries
    :param search_request: instance Search_request
    :param product_id: instance Product
    """
    try:
        phone = find_phone(product_id, 'lk')
        registration(driver, phone.phone_number)
        sleep(uniform(1.15, 1.51))
        find_by_request(driver, search_request.request)
        look_random_products(driver)
        go_on_product_page(driver, product_id.id_product)
        try:
            driver.find_elements_by_class_name('to-poned')[0].click()
        except Exception as e:
            print(e)

        action_question = ActionWithProduct.objects.create(action_type='lk',
                                                           phone_number_id=phone.id,
                                                           product_id=product_id.id,
                                                           search_request=search_request)
        phone.rn_phone_inside_action_with_product.add(action_question)

    except Exception as e:
        print(e)


def ask_questions(driver, search_request, product_id, question: str):
    """
    by product id find by search requests, browses several random products,go on product page ans asl question
    :param driver: instance selenium webdriver logout wildberries
    :param search_request: instance Search_request
    :param product_id: instance Product
    :param question:
    :return:
    """
    try:
        phone = find_phone(product_id.id_product, 'qs')
        registration(driver, phone.phone_number)
        find_by_request(driver, search_request.request)
        look_random_products(driver)
        go_on_product_page(driver, product_id.id_product)
        try:
            sleep(uniform(1.15, 1.51))
            footer_tabs = driver.find_element_by_class_name('comments-tabs').find_element_by_id('a-Questions')
            footer_tabs.click()
            input_field = driver.find_element_by_class_name('val-msg')
            driver.execute_script("arguments[0].scrollIntoView();", input_field)
            for i in question:
                input_field.send_keys(i)
                sleep(uniform(.15, .51))
            input_field.click()
            button_send = driver.find_element_by_class_name('post-data')
            button_send.click()
        except Exception as e:
            print(e)
        action_question = ActionWithProduct.objects.create(action_type='qw',
                                                           phone_number_id=phone,
                                                           product_id=product_id,
                                                           search_request=search_request)

        phone.rn_phone_inside_action_with_product.add(action_question)

    except Exception as e:
        print(e)


def find_phone(product_id, action_type):
    """

    :param product_id: instance Product
    :param action_type: str: lk' or 'fv' or 'bfv' or 'qs' or 'or' or 'rv'
    :return:
    """
    if action_type == 'lk' or 'fv' or 'bfv' or 'qs': # action = like OR favorites OR brand_favorites OR question
        try:
            # phone_number = Phone.objects.exclude(rn_phone_inside_action_with_product__action_type=action_type).\
            #     exclude(rn_phone_inside_action_with_product__product_id=product_id)
            # phone_number = Phone.objects.filter(status_rent='rent').
            phone_to_exclude = ActionWithProduct.objects.filter(product_id=product_id, action_type='lk', )
            phone_id_to_exclude_list = [action.phone_number_id for action in phone_to_exclude]
            phone_number = Phone.objects.exclude(pk__in=phone_id_to_exclude_list).\
                filter(status_rent='rent', end_rent_date__gte=date.today() + timedelta(minutes=10)).first()
            if not phone_number:
                phone_number = Phone.objects.exclude(pk__in=phone_id_to_exclude_list). \
                    filter(status_rent='sms', end_rent_date__gte=date.today() + timedelta(minutes=10)).first()
                if not phone_number:
                    phone_number = 1/0
        except ZeroDivisionError:
            phone_number = take_phone_from_sms_activate()
        except Exception as e:
            print(e)

    if action_type == 'or':  # action = order
        try:
            phone_number = Phone.objects.filter(rn_phone_inside_action_with_product__action_type='or',
                                                rn_phone_inside_action_with_product__created_at__lte=date.today() - timedelta(days=14),
                                                status_rent='rent',
                                                end_rent_date__gte=date.today() + timedelta(days=14)).first()
            if not phone_number:
                phone_number = Phone.objects.exclude(rn_phone_inside_action_with_product__action_type='or').\
                    filter(rn_phone_inside_action_with_product__created_at__gte=date.today() - timedelta(days=14),
                           status_rent='rent',
                           end_rent_date__gte=date.today() + timedelta(days=14)).first()
                if not phone_number:
                    # todo add prolongation for currently numbers
                    phone_number = 1/0
        except ZeroDivisionError:
            phone_number = take_phone_from_sms_activate()
        except Exception as e:
            print(e)
    if action_type == 'rv':  # action = review
        try:
            phone_number = Order.objects.filter(id_product=product_id).\
                filter(order_status='dld').exclude(phone_number__rn_phone_inside_action_with_product__action_type='rv')\
                .first().phone_number.phone_number
        except Exception as e:
            print(e)
    return phone_number


def take_phone_from_sms_activate():
    # todo add sms-activate pfone import
    phone = randint(11111111111, 99999999999)
    print('Creating random phone number')
    return phone


def change_name_profile(driver, name: list):
    """
    change first and second name in profile, for ask questions
    :param driver: instance webdriver with complete authorization
    :param name: ['first_name', 'second_name']
    """
    sleep(uniform(1.15, 1.51))
    icon_profile = driver.find_elements_by_class_name('navbar-pc__icon--profile')
    icon_profile[0].click()
    sleep(uniform(1.15, 1.51))
    icon_profile_inside_lk = driver.find_elements_by_class_name('item-profile')
    icon_profile_inside_lk[0].click()
    sleep(uniform(1.15, 1.51))
    edit_button = driver.find_elements_by_class_name('edit')
    edit_button[0].click()
    sleep(uniform(1.15, 1.51))
    inputs_name = driver.find_elements_by_class_name('input-item')
    inputs_name[0].click()
    sleep(uniform(1.15, 1.51))
    inputs_name[0].send_keys(Keys.CONTROL + "a")
    inputs_name[0].send_keys(Keys.DELETE)
    # in first field write second_name
    for i in name[1]:
        inputs_name[0].send_keys(i)
        sleep(uniform(.15, .51))

    inputs_name[1].click()
    sleep(uniform(1.15, 1.51))
    inputs_name[1].send_keys(Keys.CONTROL + "a")
    inputs_name[1].send_keys(Keys.DELETE)
    # in second field write first_name
    for i in name[0]:
        inputs_name[1].send_keys(i)
        sleep(uniform(.15, .51))

    save_button = driver.find_elements_by_class_name('c-btn-main')
    save_button[0].click()

#
# def add_brand_favorites(driver, product_id, search_request):
#     phone = find_phone(product_id.id_product, 'bfv')
#     registration(driver, phone.phone_number)
#     find_by_request(driver, search_request.request)
#     look_random_products(driver)
#     go_on_product_page(driver, product_id.id_product)
#     sleep(uniform(1.15, 1.51))
#     brand_logo = driver.find_elements_by_class_name('brand-logo')
#     brand_logo[0].click()
#     sleep(uniform(1.15, 1.51))
#
#     driver.find_element_by_class_name('i-brand-like').click()
#


def main():
    phone = Phone.objects.get(phone_number='9372268793')
    search_request = Search_request.objects.get(request='ремень')
    product_id = Product.objects.get(id_product='6109083') # 6109083 26541585
    size = '110'
    delivery_method = 'courier'  # or point

    # todo сделать скрипт для постановки лайка бренду
    # todo скрипт добавления в избранное

    # todo добавить выбор номера для заказа и добавления действия в корзину
    # todo сделать скрипт проверки статуса

    name = ('Вася', 'Пупкин')
    addresses = ('Саратовская область', 'г Балаково', 'Саратовское Шоссе', '39')
    question = 'Когда будет новое поступление?'
    flat = '123'
    private_house = True
    driver_obj = Chromedriver()
    driver = driver_obj.start_driver(str(bd) + '/chromedriver')


    registration(driver, phone.phone_number)
    # change_name_profile(driver, name)
    find_by_request(driver, search_request.request)
    look_random_products(driver)
    go_on_product_page(driver, product_id.id_product)

    put_like_the_product(driver, search_request, product_id)
    ask_questions(driver, search_request, product_id.id_product, question)
    make_order(driver, addresses, product_id, size,
    delivery_method, flat, private_house, name, phone, search_request)

    driver.quit()


if __name__ == '__main__':
    main()

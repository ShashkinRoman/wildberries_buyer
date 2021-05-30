import os
import requests
from dotenv import load_dotenv
from maker_orders.models import Phone
load_dotenv()


key = os.getenv('SMS_ACTIVATE_KEY')


def get_balance(key):
    balance_str = requests.get(f'https://sms-activate.ru/stubs/handler_api.php?api_key=${key}&action=getBalance').text
    balance = float(balance_str.split('ACCESS_BALANCE:')[1])
    return balance


def get_new_phone_number(key, service='uu', time_rent='4', webhook_url=''):
    """
    get new phone number from sms-activate max len time_rent 56*24 = 1344
    :param key:
    :param service: for wildverries 'uu'
    :param time: quantity hours in string min 4 hours
    :param webhook_url: url for web hook in string
    :return: phone number in string uu'79881998465
    """

    if webhook_url != '':
        url_for_rent = f'https://sms-activate.ru/stubs/handler_api.php?' \
                       f'api_key={key}&action=getRentNumber&service={service}&' \
                       f'rent_time={time_rent}&&url={webhook_url}'
    else:
        url_for_rent = f'https://sms-activate.ru/stubs/handler_api.php?api_key={key}' \
                       f'&action=getRentNumber&service={service}&rent_time={time_rent}'
    try:
        response = requests.get(url_for_rent).json()
        if response.get('status') == 'success':
            Phone.objects.create(id_rent=response.get('phone').get('id'),
                                 phone_number=response.get('phone').get('number'),
                                 end_rent_date=response.get('phone').get('endDate'),
                                 status_rent='rent')
        if response.get('status') == 'error':
            pass
    except Exception as e:
        print(response)
        print(e)
    return response.get('phone').get('number'),


def get_currently_rent(key):
    """
    :param key:
    :return: json with rent
    """
    responce_rent = requests.get(f'http://sms-activate.ru/stubs/handler_api.php?api_key={key}&action=getRentList').json()
    return responce_rent.get('values')


def get_status_for_rent(key, id_rent):
    """ success only when sms quantity > 0"""
    response_status_rent = requests.get(f'https://sms-activate.ru/stubs/handler_api.php?'
                                        f'api_key={key}&action=getRentStatus&id={id_rent}').json()
    return response_status_rent


def get_code(key, phone):
    """
    get code for authorization
    :param key: token sms-activate
    :param phone: instance Phone
    :return:
    """
    id_rent = phone.id_rent
    response_status_rent = requests.get(f'https://sms-activate.ru/stubs/handler_api.php?'
                                        f'api_key={key}&action=getRentStatus&id={id_rent}').json()
    sms_text = response_status_rent.get('values').get('0').get('text')
    code = sms_text.split('Kod podtverzhdeniya vhoda v LK ')[1].split('.')[0]
    return code

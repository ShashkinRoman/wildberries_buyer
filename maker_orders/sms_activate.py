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


def get_new_phone_number(key, service='uu', time_rent='1', webhook_url=''):
    """
    get new phone number from sms-activate max len time_rent 56*24 = 1344
    :param key:
    :param service: for wildverries 'uu'
    :param time: quantity hours in string
    :param webhook_url: url for web hook in string
    :return: phone number in string uu'79881998465
    """

    if webhook_url != '':
        url_for_rent = f'https://sms-activate.ru/stubs/handler_api.php?api_key={key}&action=getRentNumber&service={service}&rent_time={time_rent}&&url={webhook_url}'
    else:
        url_for_rent = f'https://sms-activate.ru/stubs/handler_api.php?api_key={key}&action=getRentNumber&service={service}&rent_time={time_rent}'
    try:
        response = requests.get(url_for_rent).json()
        Phone.objects.create(id_rent=response.get('phone').get('id'),
                             phone_number=response.get('phone').get('number'),
                             end_rent_date=response.get('phone').get('endDate'))
    except Exception as e:
        print(response)
        print(e)
    return response.get('phone').get('number')


def get_cirrently_rent(key):
    """
    :param key:
    :return: json with rent
    """
    responce_rent = requests.get(f'http://sms-activate.ru/stubs/handler_api.php?api_key={key}&action=getRentList').json()
    return responce_rent

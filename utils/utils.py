import requests
import json
import hashlib
from typing import Any, List, Dict
from django.conf import settings

from ..conf import conf


api_key = getattr(settings, 'FASTFOREX_API_KEY')
api_url = getattr(settings, 'FASTFOREX_API_URL')


def get_payment_system(currency_id: str) -> List[str]:
    for payment in conf.payment_systems:
        if payment.get('currency_id') == currency_id:
            return payment.get('payment_system')


def currency_convertor(currency_id: str, amount: float) -> float:
    uri_string = f'convert?from=EUR&to={currency_id}&amount={amount}&api_key={api_key}'
    url = f'{api_url}/{uri_string}'
    headers = {"accept": "application/json"}
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    return res.json().get('result').get(currency_id)


def get_currensies_rate():
    uri_string = f'fetch-multi?from=EUR&to=INR,KHR,MMK,BDT,KES,NPR,PKR,TND&api_key={api_key}'
    url = f'{api_url}/{uri_string}'
    headers = {"accept": "application/json"}
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    return res.json().get('results')


def check_transactions_hash(
        transactions: List[Dict[Any, Any]],
        webhook_access_key: str,
        webhook_private_key: str,
        transaction_signature, **kwargs) -> bool:
    transactions_json = json.dumps(
        transactions,
        ensure_ascii=False,
        separators=(',', ':'))
    md5_hash = hashlib.md5(transactions_json.encode('utf-8')).hexdigest()
    signature = hashlib.sha1((
        webhook_access_key + webhook_private_key + md5_hash).encode('utf-8')).hexdigest()
    if signature != transaction_signature:
        raise Exception('Hash is not valid - invoive %s' % kwargs.get('invoice'))

from dataclasses import dataclass
import json
from typing import Dict, Any, List
from requests import request, RequestException
import logging

LOG = logging.getLogger(__name__)

@dataclass
class Payment:
    api_key: str
    api_url: str

    def __auth_request(
            self,
            method: str,
            path: str,
            data: Dict[str, Any]) -> Dict[Any, Any]:
        headers = {
            'apikey': self.api_key,
            'Content-Type': 'application/json'
            }
        if method == 'POST':
            payload = json.dumps(data)
            try:
                response = request(
                    method="POST",
                    url=f"{self.api_url}/{path}",
                    headers=headers,
                    data=payload)
                return response.json()
            except Exception as err:
                LOG.error(err)

    def create(
            self,
            amount: float,
            currency: str,
            invoice_id: str,
            user_id: str,
            return_url: str,
            webhook_id: int,
            payment_system: List[str]) -> Dict[Any, Any]:
        path = 'Remotes/create-payment-page'
        data = {
            'language': 'EN',
            'amount': amount,
            'currency': currency,
            'payment_system': payment_system,
            'custom_transaction_id': invoice_id,
            'custom_user_id': user_id,
            'return_url': return_url,
            'webhook_id': webhook_id,
            'data': {
                'phone_number': "254712345678"
                }
        }
        res = self.__auth_request(path=path, method='POST', data=data)
        if res.get('success'):
            return res.get('url')
        raise RequestException(res.get('message'))

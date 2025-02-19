from django.conf import settings


class Conf(object):
    def __init__(self):
        self.paykassma_settings = getattr(settings, 'PAYKASSMA_SETTINGS', {})
        self.api_key = self.paykassma_settings.get('api_key')
        self.return_url = self.paykassma_settings.get('return_url')
        self.api_url = self.paykassma_settings.get('api_url')
        self.webhook_id = self.paykassma_settings.get('webhook_id')
        self.payment_systems = [
            {
                "currency_name": "Rupee",
                "currency_id": "INR",
                "payment_system": ["phonepe", "upi_p2p", "paytm"]
            },
            {
                "currency_name": "Cambodian Riel",
                "currency_id": "KHR",
                "payment_system": ["wing_l"]
            },
            {
                "currency_name": "Myanmar Kyat",
                "currency_id": "MMK",
                "payment_system": ["wavepay_l"]
            },
            {
                "currency_name": "Bangladeshi Taka",
                "currency_id": "BDT",
                "payment_system": ["nagad_a"]
            },
            {
                "currency_name": "Kenyan Shilling",
                "currency_id": "KES",
                "payment_system": ["mpesa"]
            },
            {
                "currency_name": "Nepalese Rupee",
                "currency_id": "NPR",
                "payment_system": ["khalti"]
            },
            {
                "currency_name": "Pakistani Rupee",
                "currency_id": "PKR",
                "payment_system": ["jazzcash_l", "jazzcash_fast", "nayapay_l"]
            },
            {
                "currency_name": "Tunisian Dinar",
                "currency_id": "TND",
                "payment_system": ["flouci"]
            }
        ]

    def get_payment_system(self, currency_id: str):
        for payment in self.payment_systems:
            if payment.get('currency_id') == currency_id:
                return payment.get('payment_system')


conf = Conf()

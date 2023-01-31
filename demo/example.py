import requests
import json
import sys
import os
import time
from datetime import datetime as dt, timedelta as td
from dotenv import dotenv_values

# === logging
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("tgbot")

# === config
app_config = os.getenv("APP_CONFIG",f"{os.path.dirname(__file__)}/../env/local/api.env")
logger.debug(f"app_config: {app_config}")
from dotenv import dotenv_values
config = {
    **dotenv_values(app_config),  # load shared development variables
    **os.environ,  # override loaded values with environment variables
}


class RapaygoClient:

  
    def __init__(self,api_key, api_secret, name):

        # self.session = requests.Session()
        # self.a = requests.adapters.HTTPAdapter(max_retries=3, pool_connections = 3, pool_maxsize = 30, pool_block = False)
        # requests.mount('http://', self.a)
        # requests.mount('https://', self.a)

        self.name = name
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = config['RAPAYGO_BASE_URL']
    


    async def init(self):
        self.auth = await self._auth(self.api_key, self.api_secret)
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": self.auth['access_token']
        }

    async def _auth(self, key, secret):

        url = f"{self.base_url}/auth/key"

        payload = json.dumps({
            "key": key,
            "secret": secret
        })

        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        logger.debug(f"auth response: {response.text}")

        return response.json()



    async def _get(self, url):
        return requests.get(url, headers=self.headers)


    async def _post(self, url, payload):
        return requests.post(url, headers=self.headers, data=payload)

    async def _put(self, url, payload):
        return requests.put(url, headers=self.headers, data=payload)

    async def _delete(self, url):
        return requests.delete(url, headers=self.headers)
    
    async def create_invoice(self, amount_sats, memo):
        url = f"{self.base_url}/invoice_payment/ln/invoice"

        payload = json.dumps({
            "amount_sats": amount_sats,
            "memo": memo
        })
        response = await self._post(url, payload)
        return response.json()

    async def get_invoice(self, payment_hash):
        url = f"{self.base_url}/invoice_payment/by_payment_hash/{payment_hash}"
        response = await self._get(url)
        # print(response.text)
        return response.json()

    async def get_invoice_qr(self, payment_request):
        url = f"{self.base_url}/invoice_payment/ln/invoice/qr/{payment_request}"
        response = await self._get(url)
        return response.json()

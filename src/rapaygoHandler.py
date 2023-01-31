import logging
import json
import requests

import queue
import threading

from . import qr

thread_message_queue = queue.Queue()



class rapaygoHandler:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.auth_token = self.get_access_token(api_key, api_secret)

        if self.auth_token is None:
            logging.error("Error getting access token")
            self = None



    def get_access_token(self, api_key, api_secret):
        url = "https://api.rapaygo.com/v1/auth/key"

        payload = {
            "key": api_key,
            "secret": api_secret,
        }

        response = requests.request("POST", url, headers={}, data=json.dumps(payload))
        if response.status_code != 200:
            # TODO: handle error
            logging.error("Error getting access token: %s", response.text)
            return None

        return json.loads(response.text)['access_token']



    def wait_for_payment(self):
        payment_status_url = f"https://api.rapaygo.com/v1/invoice_payment/{hash}"

        # payload = {
        #     "amount_sats": amount_sats,
        #     "memo": memo
        # }
        # TODO - why is this needed?
        payload = {}
        payload = json.dumps(payload)

        headers = {'Authorization': self.auth_token}
        response = requests.request("GET", payment_status_url, headers=headers, data=payload)

        # ...



    def create_invoice(self, amount_sats, memo):
        url = "https://api.rapaygo.com/v1/invoice_payment/ln/invoice"

        payload = {
            "amount_sats": amount_sats,
            "memo": memo}

        headers = {'Authorization': self.auth_token}
        invoice = requests.request("POST", url, headers=headers, data=json.dumps(payload))

        invoice = json.loads(invoice.text)
        logging.debug("Invoice: %s", invoice.text)

        if invoice is None:
            # TODO improve this
            logging.error("Error creating invoice")
            return None
        
        qr.generate_qr_code(invoice['payment_request'], f"./invoice_qr/{invoice['payment_hash']}.png")

        self.hash = invoice['payment_hash']

        t = threading.Thread(target=self.wait_for_payment)
        t.start()

        # rrr = json.loads(response.text)
        # print(rrr)
        # print()
        # print(rrr['status'])

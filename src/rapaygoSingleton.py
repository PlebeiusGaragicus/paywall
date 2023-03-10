import logging
import json
import requests
import time

import io
import qrcode
from PIL import Image

from queue import Queue, Empty

class rapaygoException(Exception):
    def __init__(self, message):
        self.message = message



class rapaygoPaymentCancelled(Exception):
    def __init__(self, message):
        self.message = message


class rapaygoPaymentTimeout(Exception):
    def __init__(self, message):
        self.message = message



class rapaygoSingleton:
    """
    - This is an invoice "singleton" class, it will generate a single invoice at a time.
    - Use it to block execution until the invoice is paid.
    - It can also block with a timeout, but this is not recommended because a payment may be sent
        near the end of the timeout andnot be registered as recieved thereby wasting the payer's money.

    Example usage:
    ```
        rapaygo = rapaygoSingleton(key, secret)
        rapaygo.create_invoice(amount, memo)
        rapaygo.generate_qr_code() # display to user
        rapaygo.block_for_payment()
    ```

    """
    def __init__(self, api_key, api_secret, threading_message_queue: Queue=None):
        logging.debug("Initializing rapaygoHandler")
        logging.debug("api_key: %s", api_key)
        logging.debug("api_secret: %s", api_secret)
        # self.api_key = api_key
        # self.api_secret = api_secret

        # This is for cancelling invoices once blocking has started
        self.threading_message_queue = threading_message_queue

        self.auth_token = self._get_access_token(api_key, api_secret)
        logging.debug("access token: %s", self.auth_token)


    ################################################
    def _get_access_token(self, api_key, api_secret):
        url = "https://api.rapaygo.com/v1/auth/key"

        payload = {
            "key": api_key,
            "secret": api_secret,
        }

        response = requests.request("POST", url, headers={}, data=json.dumps(payload))
        if response.status_code != 200:
            logging.error("Error getting access token: response.code=%s, response.text=%d", response.code, response.text)
            raise rapaygoException(f"Error getting access token; {response.status_code=}, {response.text=}")

        return json.loads(response.text)['access_token']

    def generate_qr_code(self, box_size=6, border=1):
        qr = qrcode.QRCode(version=1, box_size=box_size, border=border)
        qr.add_data(self.invoice['payment_request'])
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        return Image.open(buffer)


    ################################################
    def create_invoice(self, amount_sats, memo):
        url = "https://api.rapaygo.com/v1/invoice_payment/ln/invoice"

        payload = {
            "amount_sats": amount_sats,
            "memo": memo
        }
        headers = {'Authorization': self.auth_token}

        res = requests.request("POST", url, headers=headers, data=json.dumps(payload))
        logging.debug("res.status_code=%d", res.status_code)

        try:
            invoice = json.loads(res.text)
        except json.decoder.JSONDecodeError as e:
            logging.error("Error decoding response: %s", e)
            raise rapaygoException(f"Error decoding invoice response: {e}")

        logging.debug("Invoice: %s", invoice)
        self.invoice = invoice
        self.payment_hash = invoice['payment_hash']


    ################################################
    def block_for_payment_timeout(self, timeout=300):
        """ TODO: I should incorporate a count-down timer here, so that the user can see how much time is left before the payment expires.
            ... also.. what if the payment goes thru seconds after it "expires"?  They basically paid for nothing.

            raises rapaygoPaymentTimeout if payment is not confirmed within ```timeout``` seconds

            example:
            ```
            try:
                if rapaygo.block_for_payment_timeout() == True:
                    pywebio.output.put_text("Payment Received!")
            except rapaygoPaymentTimeout:
                pywebio.output.put_text("NO PAYMENT!")
            ```
        """

        payment_status_url = f"https://api.rapaygo.com/v1/invoice_payment/{self.payment_hash}"

        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                response = requests.request("GET", payment_status_url, headers={'Authorization': self.auth_token}, data={})
                logging.debug("response.status_code=%d", response.status_code)

                invoice = json.loads(response.text)
                logging.debug("invoice: %s", invoice)
                if invoice['status'] == "COMPLETED":
                    return True

                logging.debug("Waiting for payment confirmation... %s", invoice['status'])

            except requests.exceptions.RequestException as e:
                # An error occurred while making the request
                pass
            time.sleep( 2 )
        raise rapaygoPaymentTimeout(f"Failed to get payment confirmation within {timeout} seconds")


    ################################################
    def block_for_payment(self):
        """
            Return True if payment is confirmed
                otherwise blocks
        """

        payment_status_url = f"https://api.rapaygo.com/v1/invoice_payment/{self.payment_hash}"

        while True:
            try:
                if self.threading_message_queue is not None:
                    try:
                        message = self.threading_message_queue.get(block=False)
                        logging.debug("message: %s", message)
                        if message == "cancel":
                            logging.debug("Canceling payment")
                            raise rapaygoPaymentCancelled("Payment cancelled by user")
                    except Empty:
                        pass


                response = requests.request("GET", payment_status_url, headers={'Authorization': self.auth_token}, data={})
                logging.debug("response.status_code=%d", response.status_code)

                invoice = json.loads(response.text)
                logging.debug("invoice: %s", invoice)

                if invoice['status'] == "COMPLETED":
                    return True

                logging.debug("Waiting for payment confirmation... %s", invoice['status'])

            except requests.exceptions.RequestException as e:
                # An error occurred while making the request
                pass
            time.sleep( 2 )

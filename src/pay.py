import os
import requests
import logging
import json
import qrcode
import dotenv

def get_access_token():

    url = "https://api.rapaygo.com/v1/auth/access_token"

    payload = \
        "{\n    \"username\": \"" + \
        os.getenv('USEREMAIL') + \
        "\",\n    \"pass_phrase\": \"" + \
        os.getenv('PASSWORD') + \
        "\",\n    \"type\": \"wallet_owner\"\n}"

    headers = {}
    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code != 200:
        logging.error("Error getting access token: %s", response.text)
        return None

    return json.loads(response.text)

def create_invoice(amount_sats, memo, auth_token):
    url = "https://api.rapaygo.com/v1/invoice_payment/ln/invoice"

    payload = "{\n    \"amount_sats\": " + str(amount_sats) + ",\n    \"memo\": \"" + memo + "\"\n}"
    
    headers = {
        'Authorization': auth_token
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(f"{response.status_code=}")

    # TODO responce 201 is returned
    # if response.status_code != 200:
    #     logging.error("Error creating invoice: %s", response.text)
    #     return None

    return json.loads(response.text)


def generate_qr_code(data, filename):
    qr = qrcode.QRCode(version = 1,
                       box_size = 10,
                       border = 5)
    qr.add_data(data)
    qr.make(fit = True)
    img = qr.make_image(fill_color = 'red',
                        back_color = 'white')
    img.save(filename)



def do_invoice(amount_sats, memo) -> str:
    logging.basicConfig(level=logging.DEBUG)
    dotenv.load_dotenv()

    at = get_access_token()

    invoice = create_invoice(amount_sats, memo, auth_token=at['access_token'])

    if invoice is None:
        logging.error("Error creating invoice")
        exit(1)
    
    generate_qr_code(invoice['payment_request'], f"./invoice_qr/invoice_{invoice['payment_hash']}.png")

    return invoice['payment_hash']
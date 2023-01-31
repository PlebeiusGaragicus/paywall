import requests
import logging
import json

# ...
#pywebio.pin.put_input("sats", label="sats", type="number", value="100")
#pywebio.pin.put_input("memo", label="memo", type="text", value="test invoice")
#pywebio.output.put_button(label="Create Invoice", onclick=click)
# ...



def click():
    amount = pywebio.pin.pin["sats"]
    memo = pywebio.pin.pin['memo']

    pay_hash = pay.do_invoice(amount, memo)

    img = open(os.getcwd() + "/invoice_qr" + f"/{pay_hash}.png", 'rb').read()
    pywebio.output.put_image(img)
    pywebio.output.scroll_to(position=pywebio.output.Position.BOTTOM)


def get_access_token(username, password):
    url = "https://api.rapaygo.com/v1/auth/access_token"

    payload = {
        "username": username,
         "pass_phrase": password,
         "type": "wallet_owner"
    }

    headers = {}
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

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






def do_invoice(amount_sats, memo, username, password) -> str:
    at = get_access_token(username, password)

    invoice = create_invoice(amount_sats, memo, auth_token=at['access_token'])

    if invoice is None:
        logging.error("Error creating invoice")
        return None
    
    generate_qr_code(invoice['payment_request'], f"./invoice_qr/{invoice['payment_hash']}.png")

    return invoice['payment_hash']

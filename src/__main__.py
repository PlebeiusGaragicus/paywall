import os
import dotenv
import logging

import pywebio

from . import pay

### CONFIG ###
DEBUG = True

# callback
def click():
    username = pywebio.pin.pin["username"]
    password = pywebio.pin.pin["password"]

    if None in [username, password]:
        pywebio.output.toast("Please enter username and password")
        return

    amount = pywebio.pin.pin["sats"]
    memo = pywebio.pin.pin['memo']

    pay_hash = pay.do_invoice(amount, memo)

    img = open(os.getcwd() + "/invoice_qr" + f"/invoice_{pay_hash}.png", 'rb').read()
    pywebio.output.put_image(img)
    pywebio.output.scroll_to(position=pywebio.output.Position.BOTTOM)

def main():
    logging.basicConfig(level=logging.DEBUG)
    dotenv.load_dotenv()

    pywebio.output.put_html("<h1>Invoice Creator</h1>")
    pywebio.output.put_text()

    pywebio.output.put_table([
        [pywebio.pin.put_input("username", label="rapaygo username", type="text", placeholder="username", value=os.getenv('USERNAME')),
        pywebio.pin.put_input("password", label="rapaygo password", type="text", placeholder="password", value=os.getenv('PASSWORD'))]
    ])
    pywebio.output.put_markdown("---")

    pywebio.pin.put_input("sats", label="sats", type="number", value="100")
    pywebio.pin.put_input("memo", label="memo", type="text", value="text invoice")

    pywebio.output.put_button(label="Create Invoice", onclick=click)


if __name__ == "__main__":
    pywebio.start_server(main, port=80, debug=DEBUG, auto_open_webbrowser=True)

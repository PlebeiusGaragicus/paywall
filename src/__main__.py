import os
import logging

import dotenv
import pywebio

from .rapaygoSingleton import rapaygoSingleton, rapaygoException, rapaygoPaymentTimeout

### GLOBALS ###
rapaygo: rapaygoSingleton = None


### CONFIG ###
DEBUG = False



def create_invoice_extralives():
    amount = 10
    memo = "one play"

    global rapaygo
    rapaygo.create_invoice(amount, memo)


    with pywebio.output.use_scope("invoice", clear=True):
        pywebio.output.put_image( rapaygo.generate_qr_code(box_size=4, border=0) )
        pywebio.output.put_markdown("# Waiting for payment...")

    pywebio.output.scroll_to(position=pywebio.output.Position.BOTTOM)

    with pywebio.output.put_loading(color='primary'):
        rapaygo.block_for_payment()

    with pywebio.output.use_scope("invoice", clear=True):
        pywebio.output.put_markdown("# PAYMENT RECIEVED!")


    os.popen("python3 game.py")

    pywebio.output.clear("invoice")





def main():
    pywebio.output.put_html("<h1>Invoice Creator</h1>")

    pywebio.output.put_button(label="Create Invoice", onclick=create_invoice_extralives)




if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(name)s [%(levelname)s] (%(filename)s @ %(lineno)d) %(message)s",
    )
    dotenv.load_dotenv()

    key = os.getenv("API_KEY")
    secret = os.getenv("API_SECRET")

    if "" in [key, secret]:
        logging.error("API_KEY and API_SECRET must be set in .env file")
        exit(1)

    # global rapaygo
    try:
        rapaygo = rapaygoSingleton(key, secret)
    except rapaygoException as e:
        logging.error(e.message)
        exit(1)

    pywebio.start_server(main, port=80, debug=DEBUG, auto_open_webbrowser=True)

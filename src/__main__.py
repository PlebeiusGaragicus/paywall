import os
import logging

import dotenv
import pywebio

from .rapaygoHandler import rapaygoSingletonHanlder, rapaygoException, rapaygoPaymentTimeout


### GLOBALS ###
rapaygo: rapaygoSingletonHanlder = None


### CONFIG ###
DEBUG = False



def create_invoice_extralives():
    amount = 10
    memo = "Extra Lives <3"

    global rapaygo
    rapaygo.create_invoice(amount, memo)

    pywebio.output.put_image( rapaygo.generate_qr_code() )
    pywebio.output.scroll_to(position=pywebio.output.Position.BOTTOM)

    # try:
    #     if rapaygo.block_for_payment_timeout() == True:
    #         pywebio.output.put_text("Payment Received!")
    # except rapaygoPaymentTimeout:
    #     pywebio.output.put_text("NO PAYMENT!")

    rapaygo.block_for_payment()
    pywebio.output.put_markdown("# WE GOT PAID!")




def main():
    pywebio.output.put_html("<h1>Invoice Creator</h1>")

    pywebio.output.put_button(label="Extra Lives <3", onclick=create_invoice_extralives)




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
        rapaygo = rapaygoSingletonHanlder(key, secret)
    except rapaygoException as e:
        logging.error(e.message)
        exit(1)

    pywebio.start_server(main, port=80, debug=DEBUG, auto_open_webbrowser=True)

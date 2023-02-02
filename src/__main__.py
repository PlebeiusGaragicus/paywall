import os
import logging
import threading
import time
from enum import Enum, auto

from PIL import Image
import dotenv
import pywebio

from . import config

from .rapaygoSingleton import rapaygoSingleton, rapaygoException, rapaygoPaymentCancelled

""" ### SCOPES ###
- main
- create_invoice
- cancel_invoice
- invoice

"""

class InvoiceType(Enum):
    CHUCKY = auto()
    PONG = auto()
    # HUNDRED_PLAYS = auto()



def cancel_invoice():
    config.threading_message_queue.put("cancel")


def check_for_game():
    """ TODO: 
    """
    # NOTE: You can't just run "ps" pipped to grep because it will return ALL processes (including the ps pipped to grep)
    #   and will always return what you're looking for

    while True:
        procs = os.popen("ps").read()
        if config.SECRET_GAME_IS_RUNNING_FLAG not in procs:
            break
        time.sleep(1)


def create_invoice(type: InvoiceType):

    pywebio.output.clear("create_invoice")
    with pywebio.output.use_scope("cancel_invoice", clear=True):
        pywebio.output.put_button(label="CANCEL invoice", onclick=cancel_invoice, color='danger')

    # TODO - make this dynamic... I can do something cool with this...
    amount = 10
    memo = "one play"

    if config.FREE_PLAY is not True:
        global rapaygo
        rapaygo.create_invoice(amount, memo)

    with pywebio.output.use_scope("invoice", clear=True):
        if config.FREE_PLAY is not True:
            pywebio.output.put_image( rapaygo.generate_qr_code() )
        pywebio.output.put_markdown("# Waiting for payment...")

    pywebio.output.scroll_to(position=pywebio.output.Position.BOTTOM)

    with pywebio.output.put_loading(color='primary'):
        try:
            if config.FREE_PLAY is not True:
                rapaygo.block_for_payment()
        except rapaygoPaymentCancelled:
            pywebio.output.clear("invoice")
            pywebio.output.clear("cancel_invoice")
            pywebio.output.toast("Payment cancelled", color='warn')
            show_create_invoice_button()
            return

    pywebio.output.toast("Payment received!", color='success')


    with pywebio.output.use_scope("invoice", clear=True):
        pywebio.output.put_markdown("# PAYMENT RECIEVED!")
        pywebio.output.put_text("... launching game ...")

    pywebio.output.clear("cancel_invoice")

    if type == InvoiceType.CHUCKY:
        os.popen(f"python3 chucky.py {config.SECRET_GAME_IS_RUNNING_FLAG}")
    elif type == InvoiceType.PONG:
        os.popen(f"python3 pong.py {config.SECRET_GAME_IS_RUNNING_FLAG}")

    # TODO: I don't want the user to be able to create another invoice until the game is over
    # maybe I could have another thread that blocks here and waits for no game to be running
    # a thread that checks for the game process to be running

    t = threading.Thread(target=check_for_game)
    t.start()
    t.join()

    pywebio.output.clear("invoice")
    show_create_invoice_button()


@pywebio.output.use_scope("create_invoice")
def show_create_invoice_button():

    ci = Image.open( os.getcwd() + "/assets/scrn/chucky.png" )
    ci = ci.resize((300, 300))

    pi = Image.open( os.getcwd() + "/assets/scrn/pong.png" )
    pi = pi.resize((300, 300))

    pywebio.output.put_table([[
        pywebio.output.put_column([
        pywebio.output.put_image(ci, format='png'),
        pywebio.output.put_button(label="PLAY Chucky", onclick=lambda: create_invoice(InvoiceType.CHUCKY))
        ]),
        pywebio.output.put_column([
        pywebio.output.put_image(pi, format='png'),
        pywebio.output.put_button(label="PLAY Pong", onclick=lambda: create_invoice(InvoiceType.PONG))
        ])
    ]])


def main():
    with pywebio.output.use_scope("main"):
        pywebio.output.put_html("<h1>Invoice Creator</h1>")

    show_create_invoice_button()



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

    try:
        rapaygo = rapaygoSingleton(key, secret, config.threading_message_queue)
    except rapaygoException as e:
        logging.error(e.message)
        exit(1)

    pywebio.start_server(main, port=80, debug=config.DEBUG, auto_open_webbrowser=True)

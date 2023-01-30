import os
import pywebio

from . import pay

### CONFIG ###
DEBUG = False

# callback
def click():
    amount = pywebio.pin.pin["sats"]
    memo = pywebio.pin.pin['memo']

    pay_hash = pay.do_invoice(amount, memo)

    img = open(os.getcwd() + "/invoice_qr" + f"/invoice_{pay_hash}.png", 'rb').read()
    pywebio.output.put_image(img)
    pywebio.output.scroll_to(position=pywebio.output.Position.BOTTOM)

def main():
    pywebio.output.put_html("<h1>Invoice Creator</h1>")
    pywebio.output.put_text()
    pywebio.pin.put_input("sats", label="sats", type="number", value="100")
    pywebio.pin.put_input("memo", label="memo", type="text", value="text invoice")

    pywebio.output.put_button(label="Create Invoice", onclick=click)


if __name__ == "__main__":
    pywebio.start_server(main, port=80, debug=DEBUG, auto_open_webbrowser=True)

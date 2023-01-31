import os
import logging
import dotenv

from .rapaygoHandler import rapaygoHandler

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    dotenv.load_dotenv()

    key = os.getenv("API_KEY")
    secret = os.getenv("API_SECRET")

    if "" in [key, secret]:
        logging.error("API_KEY and API_SECRET must be set in .env file")
        exit(1)

    rapaygo = rapaygoHandler(key, secret)
    print(f"{rapaygo.auth_token}")



"""
METHODOLOGY

memo includes 

callback once paid
- several invoices would be created
-- each with a different purpose

<insert coin>




"""
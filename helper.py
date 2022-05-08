import json
import logging
from datetime import datetime, timezone
import jwt
import requests
import re
import test as t

def set_up_logging():
    logger = logging.getLogger("Main")
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler('logfile.log')
    formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s', datefmt='%d-%m-%Y %H:%M:%S')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger

def create_token(app_id, client_id, shared_key, ttl, logger):
    now = int(datetime.now(tz=timezone.utc).timestamp())
    token = jwt.encode(payload={"iss": client_id,
                                "sub": app_id,
                                "iat": now,
                                "exp": now + ttl,
                                "aud": ['symbols', 'feed', 'orders', 'summary']},
                       key=shared_key,
                       algorithm="HS256")
    #logger.info(token) #useful to have token printed if want to manually debug using postman
    return(token)

def instrument_available(base_md_url, symbol, token, logger):
    headers = {"Authorization": "Bearer %s" % token}
    response = requests.get(base_md_url + "symbols/" + symbol, headers=headers)

    if response.status_code == 200:
        instrument = response.json()
        logger.info(f"Instrument name: {instrument['name']}, Ticker: {instrument['ticker']}"
                      f", Exchange: {instrument['exchange']}, Country: {instrument['country']}"
                      f", Instrument type: {instrument['symbolType']}")
        return True
    elif response.status_code == 404:
        logger.error("Requested financial instrument is not found or unavailable")
        return False
    else:
        logger.critical(f"instrument_available(): HTTP error status code: {response.status_code}")
        return False

def parse_quote(line, logger):
    # Uses simple regex to parse the response line quote
    line_json = line.decode('utf8')
    line_json_string = json.dumps(line_json)
    if line_json_string.find("price") >= 0:
        logger.info(line_json_string)
        if t.check_exp(line_json_string):  #Check if string contains exponent E+ and just skip if it has
            logger.warning("quote string has exponent somewhere in price so just skipping this line....")
            print("quote string has exponent somewhere in price so just skipping this line....")
            prices = {"bid_price": -1.0, "ask_price": -1.0}
        else:
            try:
                y = line_json_string.partition("bid")
                bid_ask_string = y[2]
                z = bid_ask_string.partition("ask")
                bid_string = z[0]
                ask_string = z[2]
                bid_string_values = re.findall("\d+.\d+", bid_string)
                ask_string_values = re.findall("\d+.\d+", ask_string)
                bid_price = float(bid_string_values[0])
                ask_price = float(ask_string_values[0])
                prices = {"bid_price": bid_price, "ask_price": ask_price}
            except (IndexError, ValueError):
                logger.warning("parse_quote(): regex failure: IndexError or ValueError")
                prices = {"bid_price": -1.0, "ask_price": -1.0}
    else:
        prices = {"bid_price": -1.0, "ask_price": -1.0}
    return prices


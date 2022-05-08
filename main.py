#########################################################################################
#                                                                                       #
# Example showing Velexa API to request market data for a selected financial instrument #
# Runs for length of time authorisation token is valid                                  #
# Add your app_id, client_id and shared_key.                                            #
# Choose ttl (time to live value) in seconds                                            #
# Change symbol to desired instrument symbol                                            #
#                                                                                       #
#########################################################################################
import helper as h
import requests
import time

logger = h.set_up_logging()  # set up some logging

# Use your secrets here and create authorisation token
app_id = ""
client_id = ""
shared_key = ""
ttl = 30  # time to live value in seconds of authorisation token
token = h.create_token(app_id, client_id, shared_key, ttl, logger)

symbol = "AAPL.NASDAQ"
#symbol = "BTC.USD"
base_md_url = "https://api-demo.exante.eu/md/3.0/"
if h.instrument_available(base_md_url, symbol, token, logger):
    # Get quote stream for requested instrument
    headers = {"Accept": "text/event-stream", "Authorization": "Bearer %s" % token}
    response = requests.get(base_md_url + "feed/" + symbol, headers=headers, stream=True)
    start_time = time.time()
    if response.status_code == 200:
        for line in response.iter_lines():
            current_time = time.time()
            elapsed_time = int(current_time - start_time)
            if elapsed_time > ttl:
                print("Current authorisation token expired")
                logger.info("Current authorisation token expired")
                break
            prices = h.parse_quote(line, logger)
            if prices.get('bid_price') >= 0:
                print(f"{symbol} bid price is {prices['bid_price']}, ask price is {prices['ask_price']}")
                logger.info(f"{symbol} bid price: {prices['bid_price']}, ask price: {prices['ask_price']}")
    else:
        logger.critical(f"HTTP error status code when requesting quote stream: {response.status_code}")
        print(f"HTTP error status code when requesting quote stream: {response.status_code}")
else:
    print(f"instrument {symbol} is not available")
    logger.info(f"instrument {symbol} is not available")

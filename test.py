import re

# line_json_string = "data:{\"timestamp\":1651919524818,\"symbolId\":\"BTC.USD\",\"bid\":[{\"price\":\"3.6E+4\",\"size\":\"0.02\"}],\"ask\":[{\"price\":\"36012\",\"size\":\"0.47\"}]}"
# line_json_string = "data:{\"timestamp\":1651409908341,\"symbolId\":\"BTC.USD\",\"bid\":[{\"price\":\"37952.5\",\"size\":\"0.04\"}],\"ask\":[{\"price\":\"37957.5\",\"size\":\"0.26\"}]}"
# line_json_string = "data:{\"timestamp\":1651506151995,\"symbolId\":\"AAPL.NASDAQ\",\"bid\":[{\"price\":\"155.5\",\"size\":\"4E+2\"}],\"ask\":[{\"price\":\"155.5\",\"size\":\"1E+2\"}]}"
# line_json_string = "data:{\"timestamp\":1651921299048,\"symbolId\":\"BTC.USD\",\"bid\":[{\"price\":\"3.605E+4\",\"size\":\"0.3\"}],\"ask\":[{\"price\":\"36059.5\",\"size\":\"0.13\"}]}"
# line_json_string = "data:{\"timestamp\":1651921299048,\"symbolId\":\"BTC.USD\",\"bid\":[{\"price\":\"36050\",\"size\":\"0.3\"}],\"ask\":[{\"price\":\"3.6E+4\",\"size\":\"0.13\"}]}"
# line_json_string = "data:{\"timestamp\":1651921299048,\"symbolId\":\"BTC.USD\",\"bid\":[{\"price\":\"36050\",\"size\":\"0.3\"}],\"ask\":[{\"price\":\"3.6059.5\",\"size\":\"0.13\"}]}"

def check_exp(line_json_string):
    match = re.search('\dE\\+', line_json_string)
    if match:  # found E+ somewhere in string
        y = line_json_string.partition("bid")  # y[2] is line containing bid and ask prices
        bid_ask_string = y[2]
        z = bid_ask_string.partition("ask")  # z[0] is bid price and size string, z[2] is ask price and size string
        bid_string = z[0]
        ask_string = z[2]
        match = re.search('\dE\\+', bid_string)
        if match:  # found E+ in bid string
            result = is_exp_in_price(bid_string)
        elif re.search('\dE\\+', ask_string):  # found E+ in ask string
            result = is_exp_in_price(ask_string)
        else:  # E+ is in different part of string
            result = False
    else:
        result = False
    return result


def is_exp_in_price(price_size_string):
    string_split = price_size_string.partition("size")
    # check if E+ is in price
    match = re.search('\dE\\+', string_split[0])
    if match:  # found match in price
        return True
    else:
        return False

# outcome = check_exp(line_json_string)
# print(f"outcome is {outcome}")

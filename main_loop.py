import bitmex
import time
from bitmex import bitmex
from configuration import *
from strategy import Strategy
from trader import Trader
import json
import operator
import sys

client = bitmex(test=TEST_EXCHANGE, api_key=API_KEY, api_secret=API_SECRET)
strategy = Strategy(client, timeframe=TIMEFRAME)
trader = Trader(client, strategy, money_to_trade=AMOUNT_MONEY_TO_TRADE, leverage=LEVERAGE)

while True:
    positions = client.Position.Position_get(filter=json.dumps({"symbol": 'XBTUSD'})).result() #check if there is an open position
    positions = positions[0]

    for position in positions:
        position_open = {}
        position_open["amount"] = str(position["currentQty"]).split("L")[0]



    if str(position_open["amount"]) == "0": #if there isnt an open position

        trader.execute_trade()
        time.sleep(1)
    else:
        print('there is an open position')
        time.sleep(1)


class Trader():
    def __init__(self, client, strategy, money_to_trade=100, leverage=5):
        self.client = client
        self.strategy = strategy

        self.money_to_trade = money_to_trade
        self.leverage = leverage

    def execute_trade(self):
        req = self.strategy.orderbook_req()

        print(f"Last volume req: {req}")

        try:

            if req == 1:
                response = self.client.Order.Order_new(
                    symbol="XBTUSD",
                    side="Buy",
                    orderQty=self.money_to_trade * self.leverage,
                ).result()
                positions = self.client.Position.Position_get(filter=json.dumps({"symbol": 'XBTUSD'})).result()[0]

                for position in positions:
                    position_open = {}
                    position_open["avgEntryPrice"] = str(position["avgEntryPrice"]).split("L")[0]
                    stop_price = round(float(position_open['avgEntryPrice']) * 0.998)
                    sell_price = round(float(position_open['avgEntryPrice']) * 1.002)
                    sell2_price = round(float(position_open['avgEntryPrice']) * 1.001)

                self.client.Order.Order_new(
                    symbol="XBTUSD",
                    side="Sell",
                    stopPx=stop_price,
                    orderQty=AMOUNT_MONEY_TO_TRADE,
                ).result()
                self.client.Order.Order_new(
                    symbol="XBTUSD",
                    side="Sell",
                    price=sell_price,
                    orderQty=AMOUNT_MONEY_TO_TRADE,
                ).result()
                #timer to wait 10 seconds
                time_to_sleep = 10
                while time_to_sleep > 0:
                    time_to_sleep = time_to_sleep - 1
                    time.sleep(1)

                try:
                    open_sell = self.client.Order.Order_getOrders(symbol='XBTUSD', reverse=False,
                                                         filter=json.dumps({"open": True})).result()[0]
                    for x in open_sell:
                        x_open = {}
                        x_open["orderID"] = str(x["orderID"]).split("L")[0]
                    cancel_by_id = self.client.Order.Order_cancel(orderID=x_open['orderID']).result()
                    self.client.Order.Order_new(
                        symbol="XBTUSD",
                        side="Sell",
                        price=sell2_price,
                        orderQty=AMOUNT_MONEY_TO_TRADE,
                    ).result()
                except Exception as e:
                    pass


            else:
                print('waiting for requirements of orderbook ')
        except Exception as e:
            print("Something goes wrong!")

        return

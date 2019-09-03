import pandas as pd
import time


class Strategy():
    def __init__(self, client, timeframe='5m'):
        self.client = client
        self.timeframe = timeframe

    def orderbook_req(self):

        prices_now = pd.DataFrame(self.client.Trade.Trade_getBucketed(  # get 24 candles with unfinished one
            binSize='1h',
            partial=True,
            symbol='XBTUSD',
            count=24,
            reverse=True
        ).result()[0])
        prices_now.set_index(['close'], inplace=True)
        delta = (prices_now['high'].max() - prices_now['low'].min()) / prices_now['low'].min()
        print(delta)

        if delta < 0.03:

            time_to_sleep = 10
            seconds_true = 0

            while time_to_sleep > 0:
                time_to_sleep = time_to_sleep - 1
                percent = 0.005
                percent_2 = 0.002

                order_book = pd.DataFrame(self.client.OrderBook.OrderBook_getL2(  #get orderbook

                    symbol='XBTUSD',
                    depth=0
                    # 0 is full depth, using 200-300 we can adjust speed from 0.5 seconds to 0.1 (depends from bitmex)

                ).result()[0])
                order_book.set_index(['price', 'size', 'side'], inplace=False)
                price_first_bid = order_book.loc[order_book[order_book.side == 'Buy'].index[0], 'price']
                price_percented = price_first_bid - (percent * price_first_bid)
                price_percented_rounded = round(price_percented)  # round it to find in dataframe.

                # find all buy from first to price_percented
                df_volume = order_book.set_index('price').loc[price_first_bid: price_percented_rounded]
                total = df_volume['size'].sum()
                price_0_2 = price_first_bid + (percent_2 * price_first_bid)
                price_0_2_rounded = round(price_0_2)

                #find and sum volume from dataframe
                df_volume2 = order_book.set_index('price').loc[price_0_2_rounded: price_first_bid]
                total2 = df_volume2['size'].sum()

                if total > 1500000 and total > total2 * 4:
                    seconds_true = seconds_true + 1
                    #for how long criterias are met
                    print(seconds_true)
                    if seconds_true == 10:
                        return 1
                else:
                    #if one time found that didnt - one more time
                    seconds_true = 0


                time.sleep(1)







            else:
                print('requirements of volume arent met ')
                return 0
        else:
            print("delta is bigger that 3%")
            return 0

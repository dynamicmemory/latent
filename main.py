import os as os 
import requests as r
import datetime as dt
import csv as csv 
from exchange import Exchange as e
from database import Database as d

base: str = "https://api.bybit.com"
tickers: str = "/v5/market/tickers"
kline: str = "/v5/market/kline"
bitcoin: str = "BTCUSDT"

def get_current_price(symbol: str) -> str: 
    json: str = ""
    params: dict = {"category": "linear",
                    "symbol": symbol,
                   }
    res = r.request("GET", url=base+tickers, params=params);
    code: int = res.status_code 
    if code == 200:
        json = res.json()["result"]["list"][0]["bid1Price"]
    else:
        json = str(code)

    return json 


def convert_time(time: str) -> tuple:
    convert: float = int(time) / 1000
    temp = str(dt.datetime.fromtimestamp(convert, tz=dt.timezone.utc))

    # Current format XXXX/XX/XX XX:XX:XX+XX:XX we must break it up
    split_str: list = temp.split(" ")
    d: str = split_str[0]
    t: str = split_str[1].split("+")[0]

    return d, t


def main():
    timeframe: str = "D"
    asset: str = "bitcoin"
    fname: str = f"{asset}-{timeframe}.csv"
    bitcoin: str = "BTCUSDT"
    ex = e(bitcoin, timeframe)
    db = d(bitcoin, timeframe)
    # ex.get_ohlc(1)
    # ex.get_price()
    ls = ex.get_ohlc(1)    
    db.write_records(ls)
    print(ls)

    # if fname not in os.listdir("./"):
    #     with open(fname, "a") as file:
            # writer = csv.writer(file)
            # writer.writerow(["date,time,open,high,low,close,volume"]) 

            # ohlc = ex.get_ohlc()
            # ohlc.reverse()
            # for tf in ohlc:
                # date, time = convert_time(tf[0])
                #
                # writer.writerow([tf[0],date,time,tf[1],tf[2],tf[3],tf[4],tf[6]])
                # print(date, time, tf[1], tf[2], tf[3], tf[4], tf[6])
    # else:
    #     with open(fname, "r") as file:
    #         reader = csv.reader(file)
    #         ls = []
    #         for row in reader:
    #             ls.append(row)
    #
    #         if len(ls) == 0:
    #             # Setup the file, maybe def setup_file()
    #             pass
    #
    #         # Get the current time 
    #         current_time = dt.datetime.now(dt.timezone.utc).timestamp()*1000
    #         print(f"Current time {current_time}")
    #
    #         # Get the time from the last record
    #         last_rec_time = ls[-1][0].split(",")[0]
    #         print(f"Last record time {last_rec_time}")
    #
    #         # Get the difference between the two 
    #         time_diff = int(current_time) - int(last_rec_time)
    #         print(f"Time difference {time_diff}")
    #
    #         # Should be a map of tf to seconds or milliseconds, manual for now 
    #         tf_milliseconds = 24 * 60 * 60 * 1000
    #         print(f"Timeframe time {tf_milliseconds}")
    #
    #         # Find out how many multiples of the Timeframe is missing from records 
    #         multiples = time_diff // tf_milliseconds
            # print(f"Mutliples missing {multiples}")

if __name__ == "__main__":
    main()


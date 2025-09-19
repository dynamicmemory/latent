import requests as r
import datetime as dt

base: str = "https://api.bybit.com"
tickers: str = "/v5/market/tickers"
kline: str = "/v5/market/kline"
bitcoin: str = "BTCUSDT"

# def request(method: str, url: str, params: dict) -> dict:
#     json: dict = {}
#     res = r.request(method, url, params=params);
#     code: int = res.status_code
#     if code == 200:
#         json = res.json()
#     else: 
#         json["error"] = code
#
#     return json


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


def get_ohlc(symbol: str, interval: str) :
    params: dict = {"category": "linear", 
                    "symbol": symbol, 
                    "interval": interval,
                    }
    res = r.request("GET", url=base+kline, params=params) 
    code: int = res.status_code
    if code == 200:
        json = res.json()["result"]["list"]
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
    ohlc = get_ohlc(bitcoin, "D")
    for tf in ohlc:
        t = convert_time(tf[0])
        
        print(t[0], t[1], tf[1], tf[2], tf[3], tf[4], tf[5], tf[6])


    # btc_price: str = get_current_price(bitcoin)
    # print("Bitcoin: $"+btc_price)


if __name__ == "__main__":
    main()


from src.agent import Agent
from src.exchange import Exchange

def main():
    syntra = Agent()
    syntra.main()
    # e = Exchange("BTCUSDT", "D")
    # print(e.get_ohlc(1))
    


if __name__ == "__main__":
    main()

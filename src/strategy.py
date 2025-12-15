import pandas as pd
from src.miniML.algorithms.kmeans import Kmeans

class Strategy:
    def __init__(self, df: pd.DataFrame):
        self.data = df


    def main(self):
        self.data.drop(["sma_50", "sma_100", "sma_200", "difference", "rsi", "volume"], axis=1, inplace=True)
        # print(self.data.tail(50))

        kmeans = Kmeans(self.data["volatility"].to_numpy(), 3)
        low, med, high = kmeans.mainloop()
        # print(low, med, high) 
        # print(self.data["volatility"].to_numpy()[-1:] < low)

        last_point = self.data["volatility"].to_numpy()[-1]
        if last_point < low:
            return "low" 
        elif last_point < med:
            return "med" 
        elif last_point < high:
            return "high" 
        else:
            return "extreme"
        



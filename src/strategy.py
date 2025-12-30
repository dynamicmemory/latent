import pandas as pd
from src.miniML.algorithms.kmeans import Kmeans

class Strategy:
    def __init__(self, df: pd.DataFrame):
        self.data = df


    def main(self):
        kmeans = Kmeans(self.data["volatility"].to_numpy(), 3)
        low, med, high = kmeans.mainloop()

        current_volitility = self.data["volatility"].to_numpy()[-1]
        if current_volitility < low:
            return "low" 
        elif current_volitility < med:
            return "med" 
        elif current_volitility < high:
            return "high" 
        else:
            return "extreme"
        



import pandas as pd 
import plotly.express as px

class Features:

    def __init__(self, fname: str):
        self.fname = fname


    def everything(self):
        df = pd.read_csv(self.fname)

        df.drop(["utc", "time"], axis=1, inplace=True)
        
        df["avg"] = df["close"].rolling(200).mean()

        temp = df.drop(["open", "high", "low", "volume"], axis=1)
        
        fig = px.line(temp, x="date", y=["close", "avg"], title="Price over time")
        fig.show()
        print(df)

    

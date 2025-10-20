import pandas as pd 
import plotly.express as px

class Features:

    def __init__(self, fname: str):
        self.fname = fname


    def everything(self):
        df = pd.read_csv(self.fname)

        df.drop(["utc", "time"], axis=1, inplace=True)
        
       
        df["diff"] = df["close"] - df["open"]
        

        self.rsi(df)
        self.simple_moving_average(df, 50)
        self.simple_moving_average(df, 100)
        self.simple_moving_average(df, 200)
        y_values = ["close", "sma_50", "sma_100", "sma_200"]
        fig = px.line(df, x="date", y=y_values, title="Price over time")
        fig2 = px.line(df, x="date", y="rsi", title="Price over time")
        fig.show()
        fig2.show()
        print(df)


    def simple_moving_average(self, df: pd.DataFrame, period: int):
        """ 
        Calculates n period moving average 
        Params: 
        df = a pandas DataFrame
        period = moving average period 
        """
        sname: str = f"sma_{period}"
        df[sname] = df["close"].rolling(period).mean()

        # Backfill pre-period rows with first average value, this stops nans
        df[sname] = df[sname].fillna(df.loc[df[sname].first_valid_index(), sname])


    def rsi(self, df: pd.DataFrame):
        df["gain"] = df["diff"].where(df["diff"] >= 0, 0) 
        df["loss"] = -df["diff"].where(df["diff"] <= 0, 0) 
        df["avgGain"] = df["gain"].rolling(14).mean()
        df["avgLoss"] = df["loss"].rolling(14).mean()
        df["rs"] = df["avgGain"] / df["avgLoss"]
        df["rsi"] = 100 - 100/(1+ df["rs"])

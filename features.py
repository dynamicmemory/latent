import pandas as pd 
import plotly.express as px
import plotly.graph_objs as go
from dash import Dash, Input, Output, html, dcc

class Features:

    def __init__(self, fname: str):
        self.fname = fname


    def everything(self):
        """
        Temp function building all features inside of till finished fully
        """

        df = pd.read_csv(self.fname)

        df.drop(["utc", "time"], axis=1, inplace=True)
       
        df["diff"] = df["close"] - df["open"]

        self.rsi(df)
        self.simple_moving_average(df, 50)
        self.simple_moving_average(df, 100)
        self.simple_moving_average(df, 200)
        y_values = ["sma_50", "sma_100", "sma_200"]
        line_fig = px.line(df, x="date", y=y_values, title="Price over time")
        fig2 = px.line(df, x="date", y="rsi", title="Price over time")
        # print(df)

        # Creates candlestick chart for price
        fig = go.Figure(data=[go.Candlestick(
            x=df["date"],
            open=df["open"],
            high=df["high"],
            low=df["low"],
            close=df["close"],
        )])
        fig.update_layout(xaxis_rangeslider_visible=False)
        fig.update_yaxes(fixedrange=False)
        self.add_line(fig, df)
        

        # Dash app to visualize what I am doing to the data.
        app = Dash(__name__)
        app.layout = [ 
            html.H1("Title"),
            dcc.Graph(id="price-chart", figure=fig, style={"height": "800px"}),
            dcc.Graph(id="rsi", figure=fig2)
        ]

        app.run(debug=True)


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
        """
        Calculates the RSI for a given asset in a dataframe. 
        """
        df["gain"] = df["diff"].where(df["diff"] >= 0, 0) 
        df["loss"] = -df["diff"].where(df["diff"] <= 0, 0) 
        df["avgGain"] = df["gain"].rolling(14).mean()
        df["avgLoss"] = df["loss"].rolling(14).mean()
        df["rs"] = df["avgGain"] / df["avgLoss"]
        df["rsi"] = 100 - 100/(1+ df["rs"])
        df.drop(["gain", "loss", "avgGain", "avgLoss", "rs"], axis = 1, inplace=True)



    # ---- Chart related functions ----
    def add_line(self, fig, df: pd.DataFrame) -> None:
        averages = ["sma_50", "sma_100", "sma_200"]
        colours = ["blue", "orange", "magenta"]
        for n, avg in enumerate(averages):
            fig.add_trace(go.Scatter(x=df["date"], y=df[avg], mode="lines",
                          line=dict(width=1.5, color=colours[n]), name= avg))




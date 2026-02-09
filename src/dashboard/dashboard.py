# # ---- Chart related functions ----
# def add_line(self, fig, df: pd.DataFrame) -> None:
#     averages = ["sma_50", "sma_100", "sma_200"]
#     colours = ["blue", "orange", "magenta"]
#     for n, avg in enumerate(averages):
#         fig.add_trace(go.Scatter(x=df["date"], y=df[avg], mode="lines",
#                           line=dict(width=1.5, color=colours[n]), name= avg))
#
#     # ---------- PLOT RELATED CODE ---------------------
#     y_values = ["sma_50", "sma_100", "sma_200"]
#     line_fig = px.line(df, x="date", y=y_values, title="Price over time")
#     fig2 = px.line(df, x="date", y="rsi", title="Price over time")
#     # print(df)
#
#     # Creates candlestick chart for price
#     fig = go.Figure(data=[go.Candlestick(
#         x=df["date"],
#             open=df["open"],
#             high=df["high"],
#             low=df["low"],
#             close=df["close"],
#         )])
#     fig.update_layout(xaxis_rangeslider_visible=False)
#     fig.update_yaxes(fixedrange=False)
#     self.add_line(fig, df)
#
#
#     # ---------- DASHBOARD RELATED CODE ---------------------
#     y_values = ["sma_50", "sma_100", "sma_200"]
#     # Dash app to visualize what I am doing to the data.
#     app = Dash(__name__)
#     app.layout = [ 
#             html.H1("Title"),
#             dcc.Graph(id="price-chart", figure=fig, style={"height": "800px"}),
#             dcc.Graph(id="rsi", figure=fig2)
#         ]
#     # app.run(debug=True)
#

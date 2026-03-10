import pandas as pd
from backtest.backtest_engine import add_indicators, calculate_swings

class MarketData:

    def __init__(self, client):
        self.client = client

    @staticmethod
    def ohlcv_to_df(ohlcv):
        df = pd.DataFrame(
            ohlcv,
            columns=["timestamp","open","high","low","close","volume"]
        )

        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df = df.set_index("timestamp")

        return df

    def get_dataframe(self, symbol, timeframe="1h", limit=500):

        ohlcv = self.client.fetch_ohlcv(symbol, timeframe, limit)
        df = self.ohlcv_to_df(ohlcv)

        df = add_indicators(df)      # те же индикаторы, что в backtest
        df = calculate_swings(df)     # swing точки
        return df
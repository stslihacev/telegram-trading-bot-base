import pandas as pd


class MarketData:

    def __init__(self, client):
        self.client = client

    def fetch_ohlcv(self, symbol, timeframe="15m", limit=200):

        return self.client.fetch_ohlcv(symbol, timeframe, limit)

    @staticmethod
    def ohlcv_to_df(ohlcv):

        df = pd.DataFrame(
            ohlcv,
            columns=[
                "timestamp",
                "open",
                "high",
                "low",
                "close",
                "volume"
            ]
        )

        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

        return df

    @staticmethod
    def add_indicators(df):

        # простые индикаторы для начала
        df["ema20"] = df["close"].ewm(span=20).mean()
        df["ema50"] = df["close"].ewm(span=50).mean()

        df["volume_ma"] = df["volume"].rolling(20).mean()

        return df

    def get_dataframe(self, symbol, timeframe="15m", limit=200):
        ohlcv = self.fetch_ohlcv(symbol, timeframe, limit)
        df = self.ohlcv_to_df(ohlcv)

        # приводим типы к float
        for col in ["open", "high", "low", "close", "volume"]:
            df[col] = df[col].astype(float)

        df = self.add_indicators(df)
        return df
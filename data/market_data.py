# data/market_data.py
import pandas as pd
import pandas_ta as ta

class MarketData:
    @staticmethod
    def ohlcv_to_df(ohlcv, columns=None):
        if not columns:
            columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
        df = pd.DataFrame(ohlcv, columns=columns)
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        return df

    @staticmethod
    def add_indicators(df):
        """
        Добавляет индикаторы для стратегии.
        """
        df['ema20'] = ta.ema(df['close'], length=20)
        df['ema50'] = ta.ema(df['close'], length=50)
        df['rsi'] = ta.rsi(df['close'], length=14)
        macd = ta.macd(df['close'])
        df['macd'] = macd['MACD_12_26_9']
        df['macd_signal'] = macd['MACDs_12_26_9']
        df['atr'] = ta.atr(df['high'], df['low'], df['close'], length=14)
        return df
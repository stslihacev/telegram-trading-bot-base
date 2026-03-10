# strategy/bos_strategy_wrapper.py
from strategy.bos_strategy import BosStrategy
from data.exchange_client import BybitClient
from data.market_data import MarketData
from config.strategy_params import BOS_LOOKBACK, ATR_MULTIPLIER, RR_RATIO
import pandas as pd

class BosStrategyRunner:
    def __init__(self):
        self.strategy = BosStrategy()
        self.client = BybitClient()
    
    def get_data(self, symbol, timeframe, limit=200):
        ohlcv = self.client.fetch_ohlcv(symbol, timeframe, limit)
        df = MarketData.ohlcv_to_df(ohlcv)
        df = MarketData.add_indicators(df)
        return df
    
    def run(self, symbol, idx=None, arrays=None, swing_idx=None, diagnostics=None, entry_tf="15m"):
        """
        Возвращает сигнал BOS стратегии для указанного символа
        """
        # получаем данные
        df = self.get_data(symbol, entry_tf)
        
        if idx is None:
            idx = len(df) - 1  # последняя свеча
        if arrays is None:
            arrays = {}
        if swing_idx is None:
            swing_idx = []
        if diagnostics is None:
            diagnostics = {}

        # вызываем оригинальную стратегию
        signal = self.strategy.generate_signal(
            symbol,
            idx,
            df,
            arrays,
            swing_idx,
            diagnostics
        )

        # добавляем расчёт SL и TP
        if signal is not None and "side" in signal:
            atr = df['atr'].iloc[idx]
            entry_price = df['close'].iloc[idx]
            sl = entry_price - ATR_MULTIPLIER * atr if signal["side"] == "LONG" else entry_price + ATR_MULTIPLIER * atr
            tp = entry_price + RR_RATIO * (entry_price - sl) if signal["side"] == "LONG" else entry_price - RR_RATIO * (sl - entry_price)
            signal.update({
                "entry_price": entry_price,
                "sl": sl,
                "tp": tp,
                "time": df.index[idx]
            })

        return signal
from backtest.backtest_engine import BosStrategy, detect_bos_fast, liquidity_sweep, get_market_regime

class StrategyAdapter:

    def __init__(self):
        self.strategy = BosStrategy()

    def prepare_arrays(self, df):
        return {
            "close": df["close"].values,
            "high": df["high"].values,
            "low": df["low"].values,
            "ema200": df["ema200"].values
        }

    def prepare_swings(self, df):
        swing_low = df.index[df["swing_low"]].tolist()
        swing_high = df.index[df["swing_high"]].tolist()
        return {"low": swing_low, "high": swing_high}

    def run(self, symbol, df):

        idx = len(df) - 1

        arrays = self.prepare_arrays(df)
        swing_indices = self.prepare_swings(df)
        diagnostics = {}

        signal = self.strategy.generate_signal(
            symbol,
            idx,
            df,
            arrays,
            swing_indices,
            diagnostics
        )

        return signal
class BosStrategy:

    def __init__(self):
        pass

    def generate_signal(self, symbol, idx, df, arrays=None, swing_indices=None, diagnostics=None):

        if idx < 20:
            return None

        current_high = df["high"].iloc[idx]
        previous_high = df["high"].iloc[idx - 1]

        current_low = df["low"].iloc[idx]
        previous_low = df["low"].iloc[idx - 1]

        # Break of structure вверх
        if current_high > previous_high:
            return {
                "symbol": symbol,
                "side": "LONG",
                "entry": df["close"].iloc[idx],
                "tp": df["close"].iloc[idx] * 1.02,
                "sl": df["close"].iloc[idx] * 0.99
            }

        # Break вниз
        if current_low < previous_low:
            return {
                "symbol": symbol,
                "side": "SHORT",
                "entry": df["close"].iloc[idx],
                "tp": df["close"].iloc[idx] * 0.98,
                "sl": df["close"].iloc[idx] * 1.01
            }

        return None
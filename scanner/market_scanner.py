from strategy.strategy_adapter import StrategyAdapter
from data.market_data import MarketData
from data.exchange_client import BybitClient

class MarketScanner:

    def __init__(self):
        self.client = BybitClient()
        self.market_data = MarketData(self.client)
        self.strategy = StrategyAdapter()

    def scan_market(self):

        pairs = self.client.get_top_symbols(limit=20, min_volume=1000)

        for symbol in pairs:

            df = self.market_data.get_dataframe(symbol, timeframe="1h")

            signal = self.strategy.run(symbol, df)

            if signal:
                print("📊 СИГНАЛ:", signal)
            else:
                print(f"Сигнала по {symbol} нет.")
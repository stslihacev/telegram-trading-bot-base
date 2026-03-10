# scanner/market_scanner.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.exchange_client import BybitClient
from data.market_data import MarketData
from strategy.bos_strategy_wrapper import BosStrategyRunner
from config.settings import TOP_PAIRS_LIMIT

class MarketScanner:
    def __init__(self):
        self.client = BybitClient()
        self.runner = BosStrategyRunner()
    
    def get_top_pairs(self):
        tickers = self.client.fetch_tickers()
        volume_dict = {symbol: tickers[symbol]['quoteVolume'] for symbol in tickers if 'USDT' in symbol}
        sorted_pairs = sorted(volume_dict.items(), key=lambda x: x[1], reverse=True)
        top_pairs = [pair for pair, _ in sorted_pairs[:TOP_PAIRS_LIMIT]]
        return top_pairs

    def scan_market(self, entry_tf="15m"):
        top_pairs = self.get_top_pairs()
        signals = []
        for symbol in top_pairs:
            signal = self.runner.run(symbol, entry_tf=entry_tf)
            if signal:
                signals.append(signal)
                print(f"Сигнал найден: {signal['side']} {symbol} | Entry: {signal['entry_price']:.2f} | TP: {signal['tp']:.2f} | SL: {signal['sl']:.2f}")
        return signals

if __name__ == "__main__":
    scanner = MarketScanner()
    scanner.scan_market(entry_tf="15m")
# main.py
from strategy.bos_strategy_wrapper import BosStrategyRunner

if __name__ == "__main__":
    runner = BosStrategyRunner()
    
    # пример анализа последней свечи по BTCUSDT
    signal = runner.run("BTCUSDT", entry_tf="15m")
    
    if signal:
        print("Сигнал найден:")
        print(signal)
    else:
        print("Сигналов нет")
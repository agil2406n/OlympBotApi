import asyncio
import logging
from bot import OlympTradeBot
from config import TRADE_AMOUNT, ACCOUNT_GROUP

logger = logging.getLogger(__name__)


class AdvancedTradingBot(OlympTradeBot):
    """Gelişmiş strateji kullanan trading botu"""
    
    async def moving_average_strategy(self):
        """Hareketli Ortalama Stratejisi"""
        candles = await self.get_market_data()
        if len(candles) < 10:
            return None
        
        # Son 10 mumun kapanış fiyatları
        closes = [c['close'] for c in candles[-10:]]
        
        # 5 ve 10 günlük hareketli ortalamaları hesapla
        ma5 = sum(closes[-5:]) / 5
        ma10 = sum(closes[-10:]) / 10
        
        # Sinyal üret
        if ma5 > ma10:
            return "UP"
        elif ma5 < ma10:
            return "DOWN"
        return None
    
    async def rsi_strategy(self):
        """Relative Strength Index (RSI) Stratejisi"""
        candles = await self.get_market_data()
        if len(candles) < 15:
            return None
        
        closes = [c['close'] for c in candles]
        
        # Fiyat değişikliklerini hesapla
        deltas = [closes[i] - closes[i-1] for i in range(1, len(closes))]
        
        # Pozitif ve negatif değişiklikleri ayır
        gains = [d if d > 0 else 0 for d in deltas]
        losses = [-d if d < 0 else 0 for d in deltas]
        
        # Ortalama kazanç ve kayıp
        avg_gain = sum(gains[-14:]) / 14
        avg_loss = sum(losses[-14:]) / 14
        
        # RSI hesapla
        if avg_loss == 0:
            rsi = 100 if avg_gain > 0 else 0
        else:
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
        
        # Sinyal üret
        if rsi < 30:
            return "UP"  # Aşırı satım
        elif rsi > 70:
            return "DOWN"  # Aşırı alım
        return None
    
    async def volatility_strategy(self):
        """Volatilite Tabanlı Strateji"""
        candles = await self.get_market_data()
        if len(candles) < 5:
            return None
        
        # Yüksek ve düşük fiyatları al
        highs = [c['high'] for c in candles[-5:]]
        lows = [c['low'] for c in candles[-5:]]
        closes = [c['close'] for c in candles[-5:]]
        
        # Volatiliteyi hesapla
        volatility = (max(highs) - min(lows)) / sum(closes) * 100
        
        # Yüksek volatilitede trend takip et
        if volatility > 2:
            if closes[-1] > closes[-2]:
                return "UP"
            else:
                return "DOWN"
        return None
    
    async def run_advanced_strategy(self, strategy_name="moving_average", interval=10):
        """Gelişmiş strateji çalıştır"""
        self.is_running = True
        logger.info(f"🤖 {strategy_name} stratejisi başlatıldı...")
        
        strategies = {
            "moving_average": self.moving_average_strategy,
            "rsi": self.rsi_strategy,
            "volatility": self.volatility_strategy
        }
        
        if strategy_name not in strategies:
            logger.error(f"Strateji bulunamadı: {strategy_name}")
            return
        
        strategy_func = strategies[strategy_name]
        
        try:
            while self.is_running:
                balance = await self.get_balance()
                positions = await self.get_open_trades()
                
                logger.info(f"Bakiye: ${balance:.2f} | Açık Pozisyon: {len(positions)}")
                
                # Stratejiyi çalıştır
                signal = await strategy_func()
                
                if signal:
                    logger.info(f"📊 {strategy_name} sinyali: {signal}")
                    trade = await self.place_trade(signal)
                    
                    if trade:
                        logger.info(f"İşlem gerçekleştirildi")
                
                await asyncio.sleep(interval)
        
        except KeyboardInterrupt:
            logger.info("Bot durduruldu")
        except Exception as e:
            logger.error(f"Bot hatası: {e}")
        finally:
            self.is_running = False


async def main():
    bot = AdvancedTradingBot()
    
    connected = await bot.connect()
    if not connected:
        return
    
    try:
        # Farklı stratejileri dene
        await bot.run_advanced_strategy("moving_average", interval=10)
    except KeyboardInterrupt:
        logger.info("Program durduruldu")
    finally:
        await bot.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
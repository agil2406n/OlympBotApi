import asyncio
import logging
from olymptrade_ws import OlympTradeClient
from config import (
    OLYMPTRADE_ACCESS_TOKEN,
    TRADING_PAIR,
    TRADE_AMOUNT,
    TRADE_DURATION,
    ACCOUNT_GROUP,
    MAX_OPEN_TRADES,
    TAKE_PROFIT_PERCENT,
    STOP_LOSS_PERCENT
)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class OlympTradeBot:
    def __init__(self):
        self.client = OlympTradeClient(access_token=OLYMPTRADE_ACCESS_TOKEN)
        self.account_id = None
        self.open_trades = []
        self.is_running = False
        
    async def connect(self):
        """API'ye bağlan ve kimlik doğrula"""
        try:
            await self.client.start()
            if self.client.is_connected:
                logger.info("✓ OlympTrade API'ye başarıyla bağlandı")
                await self._get_account_info()
                return True
            else:
                logger.error("✗ API'ye bağlanılamadı")
                return False
        except Exception as e:
            logger.error(f"✗ Bağlantı hatası: {e}")
            return False
    
    async def disconnect(self):
        """API bağlantısını kes"""
        try:
            await self.client.stop()
            logger.info("✓ API bağlantısı kesildi")
        except Exception as e:
            logger.error(f"✗ Bağlantı kesme hatası: {e}")
    
    async def _get_account_info(self):
        """Hesap bilgilerini al"""
        try:
            balance = await self.client.balance.get_balance()
            demo_acc = next(acc for acc in balance['d'] if acc['group'] == ACCOUNT_GROUP)
            self.account_id = demo_acc['account_id']
            
            logger.info(f"Hesap: {self.account_id}")
            logger.info(f"Bakiye: ${demo_acc['amount']:.2f}")
            
            return demo_acc
        except Exception as e:
            logger.error(f"Hesap bilgisi alınamadı: {e}")
            return None
    
    async def get_balance(self):
        """Güncel bakiye bilgisini al"""
        try:
            balance = await self.client.balance.get_balance()
            demo_acc = next(acc for acc in balance['d'] if acc['group'] == ACCOUNT_GROUP)
            return demo_acc['amount']
        except Exception as e:
            logger.error(f"Bakiye alınamadı: {e}")
            return 0
    
    async def get_open_trades(self):
        """Açık pozisyonları getir"""
        try:
            positions = await self.client.trade.get_open_trades(self.account_id, group=ACCOUNT_GROUP)
            self.open_trades = positions
            logger.info(f"Açık pozisyon sayısı: {len(positions)}")
            return positions
        except Exception as e:
            logger.error(f"Açık pozisyonlar alınamadı: {e}")
            return []
    
    async def get_market_data(self):
        """Mum grafik verilerini al"""
        try:
            candles = await self.client.market.get_candles(TRADING_PAIR, size=60, count=10)
            return candles
        except Exception as e:
            logger.error(f"Pazar verisi alınamadı: {e}")
            return []
    
    async def place_trade(self, direction):
        """İşlem emri ver (UP/DOWN)"""
        if len(self.open_trades) >= MAX_OPEN_TRADES:
            logger.warning(f"Maksimum açık işlem sayısına ({MAX_OPEN_TRADES}) ulaşıldı")
            return None
        
        try:
            order_result = await self.client.trade.place_order(
                pair=TRADING_PAIR,
                amount=TRADE_AMOUNT,
                direction=direction.lower(),
                duration=TRADE_DURATION,
                account_id=self.account_id,
                group=ACCOUNT_GROUP
            )
            
            if order_result.get('success'):
                logger.info(f"✓ İşlem başarılı: {direction} | Miktar: ${TRADE_AMOUNT}")
                return order_result
            else:
                logger.error(f"✗ İşlem başarısız: {order_result.get('error')}")
                return None
        except Exception as e:
            logger.error(f"İşlem emri hatasında: {e}")
            return None
    
    async def close_position(self, position_id):
        """Açık pozisyonu kapat"""
        try:
            result = await self.client.trade.close_position(position_id)
            if result.get('success'):
                pnl = result.get('pnl', 0)
                logger.info(f"✓ Pozisyon kapatıldı | PnL: ${pnl:.2f}")
                return result
            else:
                logger.error(f"✗ Pozisyon kapatılmadı: {result.get('error')}")
                return None
        except Exception as e:
            logger.error(f"Pozisyon kapatma hatası: {e}")
            return None
    
    async def analyze_market(self):
        """Basit pazar analizi yap"""
        try:
            candles = await self.get_market_data()
            if len(candles) < 2:
                return None
            
            # Son iki mumu karşılaştır
            current = candles[-1]
            previous = candles[-2]
            
            current_close = current.get('close', 0)
            previous_close = previous.get('close', 0)
            
            if current_close > previous_close:
                return "UP"
            elif current_close < previous_close:
                return "DOWN"
            else:
                return None
        except Exception as e:
            logger.error(f"Market analizi hatası: {e}")
            return None
    
    async def run_trading_bot(self, interval=5):
        """Trading botunu çalıştır"""
        self.is_running = True
        logger.info("🤖 Trading botu başlatıldı...")
        
        try:
            while self.is_running:
                # Mevcut durumu kontrol et
                balance = await self.get_balance()
                positions = await self.get_open_trades()
                
                logger.info(f"Bakiye: ${balance:.2f} | Açık Pozisyon: {len(positions)}")
                
                # Pazar analizi yap
                signal = await self.analyze_market()
                
                if signal:
                    logger.info(f"📊 İşlem sinyali: {signal}")
                    trade = await self.place_trade(signal)
                    
                    if trade:
                        logger.info(f"İşlem ID: {trade.get('id')}")
                
                # Bekleme
                await asyncio.sleep(interval)
        
        except KeyboardInterrupt:
            logger.info("Bot durduruldu")
        except Exception as e:
            logger.error(f"Bot çalışma hatası: {e}")
        finally:
            self.is_running = False
    
    def stop(self):
        """Botu durdur"""
        self.is_running = False
        logger.info("Bot durduruluyor...")


async def main():
    """Ana program"""
    bot = OlympTradeBot()
    
    # API'ye bağlan
    connected = await bot.connect()
    if not connected:
        logger.error("Başlangıç başarısız")
        return
    
    try:
        # Trading botunu başlat
        await bot.run_trading_bot(interval=10)
    except KeyboardInterrupt:
        logger.info("Program durduruldu")
    finally:
        await bot.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
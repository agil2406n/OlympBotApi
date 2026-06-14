#!/usr/bin/env python3
"""
OlympTrade Bot - Hızlı Başlangıç
Basit şekilde trading botunu test etmek için kullan
"""

import asyncio
import logging
from bot import OlympTradeBot

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def quick_demo():
    """Basit demo çalıştır"""
    
    print("\n" + "="*50)
    print("🤖 OlympTrade Bot - Hızlı Demo")
    print("="*50 + "\n")
    
    bot = OlympTradeBot()
    
    # Adım 1: Bağlan
    print("[1] API'ye bağlanılıyor...")
    connected = await bot.connect()
    
    if not connected:
        print("❌ Bağlantı başarısız!")
        return
    
    print("✅ Bağlantı başarılı!\n")
    
    # Adım 2: Hesap bilgisi
    print("[2] Hesap bilgileri getiriliyor...")
    balance = await bot.get_balance()
    print(f"✅ Bakiye: ${balance:.2f}\n")
    
    # Adım 3: Açık pozisyonlar
    print("[3] Açık pozisyonlar kontrol ediliyor...")
    positions = await bot.get_open_trades()
    print(f"✅ Açık pozisyon sayısı: {len(positions)}\n")
    
    # Adım 4: Pazar verisi
    print("[4] Pazar verileri getiriliyor...")
    candles = await bot.get_market_data()
    if candles:
        last_candle = candles[-1]
        print(f"✅ Son mum kapanış: ${last_candle['close']:.2f}")
        print(f"   Yüksek: ${last_candle['high']:.2f}")
        print(f"   Düşük: ${last_candle['low']:.2f}\n")
    
    # Adım 5: Market analizi
    print("[5] Market analizi yapılıyor...")
    signal = await bot.analyze_market()
    if signal:
        print(f"✅ Sinyal: {signal}\n")
        
        # Adım 6: İşlem yap
        print("[6] Test işlemi gerçekleştiriliyor...")
        print(f"   Yön: {signal}")
        print(f"   Miktar: $1")
        print(f"   Süre: 60 saniye")
        
        trade = await bot.place_trade(signal)
        if trade:
            print("✅ İşlem başarılı!\n")
        else:
            print("❌ İşlem başarısız\n")
    else:
        print("⚠️  Net bir sinyal alınamadı\n")
    
    # Adım 7: Bağlantı kes
    print("[7] Bağlantı kesiliyor...")
    await bot.disconnect()
    print("✅ Demo tamamlandı!\n")
    
    print("="*50)
    print("✨ Bot başlatmak için: python bot.py")
    print("📊 Gelişmiş strateji için: python advanced_strategies.py")
    print("="*50 + "\n")


async def interactive_mode():
    """İnteraktif mod"""
    
    print("\n" + "="*50)
    print("🤖 OlympTrade Bot - İnteraktif Mod")
    print("="*50 + "\n")
    
    bot = OlympTradeBot()
    
    # Bağlan
    if not await bot.connect():
        print("❌ Bağlantı başarısız!")
        return
    
    print("✅ Bağlantı başarılı!\n")
    
    menu = """
    Seçenekler:
    1. Bakiye kontrol et
    2. Açık pozisyonlar
    3. İşlem yap (UP)
    4. İşlem yap (DOWN)
    5. Market analizi
    6. Çık
    
    Seçiminiz (1-6): """
    
    while True:
        try:
            choice = input(menu).strip()
            
            if choice == "1":
                balance = await bot.get_balance()
                print(f"\n💰 Bakiye: ${balance:.2f}\n")
            
            elif choice == "2":
                positions = await bot.get_open_trades()
                if positions:
                    print(f"\n📊 Açık Pozisyonlar: {len(positions)}")
                    for i, pos in enumerate(positions, 1):
                        print(f"   {i}. {pos.get('asset')}: ${pos.get('amount')}")
                else:
                    print("\n📊 Açık pozisyon yok\n")
            
            elif choice == "3":
                print("\n⏳ İşlem başlatılıyor...")
                trade = await bot.place_trade("UP")
                if trade:
                    print("✅ İşlem başarılı!\n")
                else:
                    print("❌ İşlem başarısız\n")
            
            elif choice == "4":
                print("\n⏳ İşlem başlatılıyor...")
                trade = await bot.place_trade("DOWN")
                if trade:
                    print("✅ İşlem başarılı!\n")
                else:
                    print("❌ İşlem başarısız\n")
            
            elif choice == "5":
                signal = await bot.analyze_market()
                if signal:
                    print(f"\n📊 Market Sinyali: {signal}\n")
                else:
                    print("\n📊 Net sinyal bulunamadı\n")
            
            elif choice == "6":
                break
            
            else:
                print("\n❌ Geçersiz seçim\n")
        
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"\n❌ Hata: {e}\n")
    
    await bot.disconnect()
    print("\n✅ Çıkılıyor...\n")


async def main():
    """Ana program"""
    
    print("\n" + "="*50)
    print("OlympTrade Bot Başlangıç Seçenekleri")
    print("="*50)
    
    print("\n1. Demo Çalıştır (Otomatik test)")
    print("2. İnteraktif Mod (Manüel kontrol)")
    print("3. Botu Başlat (Otomatik trading)")
    
    choice = input("\nSeçiminiz (1-3): ").strip()
    
    if choice == "1":
        await quick_demo()
    elif choice == "2":
        await interactive_mode()
    elif choice == "3":
        from bot import OlympTradeBot
        bot = OlympTradeBot()
        if await bot.connect():
            try:
                await bot.run_trading_bot()
            except KeyboardInterrupt:
                pass
            finally:
                await bot.disconnect()
    else:
        print("❌ Geçersiz seçim")


if __name__ == "__main__":
    asyncio.run(main())
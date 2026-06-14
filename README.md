# OlympTrade Trading Bot

OlympTrade API kullanarak otomatik alım-satım işlemleri gerçekleştiren bir Python bot.

## 📋 Gereksinimler

- Python 3.7+
- OlympTrade Hesabı
- API Access Token

## 🚀 Kurulum

### 1. Depo Klonla
```bash
git clone https://github.com/agil2406n/OlympBotApi.git
cd OlympBotApi
```

### 2. Bağımlılıkları Yükle
```bash
pip install -r requirements.txt
```

### 3. Çevre Değişkenlerini Ayarla
```bash
cp .env.example .env
```

`.env` dosyasını düzenle ve OlympTrade kimlik bilgilerini ekle:
```
OLYMPTRADE_ACCESS_TOKEN=your_token_here
TRADING_PAIR=LATAM_X
TRADE_AMOUNT=1
TRADE_DURATION=60
```

## 📖 Kullanım

### Hızlı Başlangıç
```bash
python quick_start.py
```

### Basit Bot Çalıştır
```bash
python bot.py
```

### Gelişmiş Stratejilerle Çalıştır
```bash
python advanced_strategies.py
```

## 🤖 Mevcut Stratejiler

### 1. **Basit Momentum Stratejisi**
- Son iki mumun kapanış fiyatlarını karşılaştırır
- Fiyat yükseliyorsa UP, düşüyorsa DOWN sinyali verir

### 2. **Hareketli Ortalama (Moving Average)**
- 5 günlük ve 10 günlük hareketli ortalamaları kullanır
- MA5 > MA10 ise UP sinyali
- MA5 < MA10 ise DOWN sinyali

### 3. **RSI (Relative Strength Index)**
- Aşırı satım (< 30) durumunda UP sinyali
- Aşırı alım (> 70) durumunda DOWN sinyali

### 4. **Volatilite Stratejisi**
- Yüksek volatilite dönemlerinde trendle takip eder

## 📊 Bot Özellikleri

✅ **Otomatik İşlem Yönetimi**
- Açık pozisyonları takip eder
- Maksimum açık işlem limitini kontrol eder

✅ **Gerçek Zamanlı Pazar Analizi**
- Mum grafik verilerini analiz eder
- Otomatik sinyal üretir

✅ **Risk Yönetimi**
- Stop loss ve take profit yüzdeleri ayarlanabilir
- Maksimum açık işlem sayısı sınırı

✅ **Detaylı Günlükleme**
- Tüm işlemleri kaydeder
- Hata ve uyarıları günlüğe yazarak

## 🔧 Konfigürasyon

`config.py` dosyasında ayarlanabilir parametreler:

```python
# İşlem Parametreleri
TRADING_PAIR = "LATAM_X"          # İşlem çifti
TRADE_AMOUNT = 1                   # İşlem miktarı
TRADE_DURATION = 60                # İşlem süresi (saniye)

# Risk Yönetimi
MAX_OPEN_TRADES = 5                # Maksimum açık işlem
STOP_LOSS_PERCENT = 10             # Zarar durdurma %
TAKE_PROFIT_PERCENT = 20           # Kar alma %
```

## 📝 Örnek Kullanım

### Basit İşlem Başlat
```python
from bot import OlympTradeBot
import asyncio

async def main():
    bot = OlympTradeBot()
    
    # API'ye bağlan
    await bot.connect()
    
    # Bakiye kontrol et
    balance = await bot.get_balance()
    print(f"Bakiye: ${balance}")
    
    # İşlem yap
    await bot.place_trade("UP")
    
    # Bağlantıyı kes
    await bot.disconnect()

asyncio.run(main())
```

### Açık Pozisyonları Kontrol Et
```python
async def check_positions():
    bot = OlympTradeBot()
    await bot.connect()
    
    positions = await bot.get_open_trades()
    for pos in positions:
        print(f"Varlık: {pos['asset']}")
        print(f"Miktar: ${pos['amount']}")
        print(f"Kar/Zarar: ${pos['pnl']}")
    
    await bot.disconnect()
```

## ⚠️ Önemli Uyarılar

⚠️ **Demo Hesap ile Başla**
- Gerçek para kullanmadan önce demo hesapta test et
- Stratejileri ve ayarları validate et

⚠️ **Risk Yönetimi**
- Maksimum açık işlem sayısını sınırla
- Stop loss ve take profit yüzdeleri ayarla
- Küçük miktarlarla başla

⚠️ **API Oranı Sınırı**
- Çok hızlı isteklerden kaçın
- Uygun aralıklarla işlem yap

## 🐛 Sorun Giderme

### "Bağlantı başarısız" hatası
```
✓ API token'ı doğru mu kontrol et
✓ İnternet bağlantısını kontrol et
✓ OlympTrade API'nin çalışıp çalışmadığını kontrol et
```

### "Hesap bulunamadı" hatası
```
✓ ACCOUNT_GROUP ayarını kontrol et
✓ Demo ya da gerçek hesabın var mı kontrol et
```

### "İşlem başarısız" hatası
```
✓ Bakiye yeterli mi kontrol et
✓ Varlık adını kontrol et
✓ İşlem süresi geçerli mi kontrol et
```

## 📚 API Referansı

### Temel Yöntemler

| Yöntem | Açıklama |
|--------|----------|
| `connect()` | API'ye bağlan |
| `disconnect()` | Bağlantıyı kes |
| `get_balance()` | Bakiye al |
| `place_trade(direction)` | İşlem yap |
| `get_open_trades()` | Açık pozisyonları al |
| `close_position(id)` | Pozisyon kapat |
| `get_market_data()` | Mum grafik verisi al |

## 📞 Destek

- [OlympTrade Resmi Sayfası](https://olymptrade.com)
- [API Dokümantasyonu](https://olymptrade.com/api)

## 📄 Lisans

Bu proje MIT lisansı altındadır.

---

**⚠️ Sorumluluk Reddi:** Bu bot eğitim amaçlı oluşturulmuştur. Finansal kaybından sorumlu değilim. Gerçek para ile kullanmadan önce iyi test edin.

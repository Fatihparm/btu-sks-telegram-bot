
#BTU-SKS-telegram
Bursa Teknik Üniversitesi öğrencileri için yemekhane menüsünü ve duyuruları takip etmeyi kolaylaştıran Telegram botudur. Bu bot, abonelik sistemi aracılığıyla günlük olarak otomatik mesajlar almanızı sağlar.

## Projenin Amacı :
Bursa Teknik Üniversitesi'nin yemekhane menüsünü pratik bir şekilde öğrenmek ve SKS (Sosyal ve Kültürel Hizmetler) duyurularını takip etmek için geliştirilmiş bir Telegram botudur.

### **Başlarken**:

- `git clone [repo]`

- `cd btu-sks-telegram-bot`

- `pip install -r requirements.txt`

- `python main.py`

### **Komutlar** :

- /menu | Bu komut, günün **yemek menüsünü** gösterir. İstenilen bir tarih belirtilmezse, komut **çalıştırıldığı günün** menüsünü gösterir.
    
    - `/menu 17` → 17. günün menüsünü gösterir.
    
    - `/menu` → Bugünün menüsünü gösterir.

- /abonelik | Bu komut, günlük olarak saat **09:00**'da içinde bulunulan günün menüsünü ve varsa yeni SKS duyurularını özel mesaj olarak almanızı sağlar. Ayrıca, **bölümünüzün adını** belirterek bölüm duyurularını da alabilirsiniz. Değer girilmezse **sadece** menü mesajları ve SKS duyuruları alırsınız
    
    - `/abonelik` → Sadece yemek menüsünü ve SKS duyurularını alırsınız.
    
    - `/abonelik bilgisayar` → Menü ve SKS duyurularının yanı sıra, bilgisayar bölümünün duyurularını da alabilirsiniz.
    
- /abonelikiptal | Var olan **aboneliğinizi iptal eder** ve bot tarafından günlük mesaj almazsınız.
    
- /duyuru | Abone **olurken** kaydolduğunuz bölümünüzün en son yüklenmiş en fazla 12 adet duyurusunu görebilirsiniz. **değer girilmezse son duyuruyu gösterir**

    - `/duyuru` → Son bölüm duyurusunu alırsınız.
    
    - `/duyuru 3` → Son 3 bölüm duyurusunu alırsınız
    
    - `/duyuru bilgisayar` → **YANLIŞ KULLANIM**

![image](/images/1.png)

![image](/images/2.png)

![image](/images/3.png)
    
![image](/images/4.png)

### **KATKI SAĞLAYANLAR**
- [Arda Aydın Kılınç](https://github.com/adraarda23)

# BTU-SKS-telegram
Telegram üzerinden okulun yemekhane menüsünü ve duyurularını takip etmemizi ve abonelik sistemiyle otomatik mesaj almamızı sağlayan telegram botu.
## Projenin Amacı : Bursa Teknik Üniversitesinin Yemek Menüsünü Pratikçe Öğrenme Botu (Telegram)
### **Başlarken**:
- `git clone [repo]`
- `cd btu-sks-telegram-bot`
- `pip install -r requirements.txt` 
- `python main.py`
### **Komutlar** : 

- /menu | menüsü öğrenilmek istenen gün **değer girilmezse o günün menüsünü gösterir**
   - `/menu 17`
   - `/menu`
- /abonelik | günlük olarak saat 09:00'da içinde olunan günün menüsünü ve eklenmişse yeni SKS duyurusunu özel mesaj olarak alırsınız. Dilerseniz **bölümünüzün adını** da girerek bölüm duyuru sayfanızdaki yeni duyuruları alabilir ve /duyuru komutunu kullanabilirsiniz. Değer girilmezse sadece menü mesajları alırsınız  
   - `/abonelik bilgisayar`
   - `/abonelik`
- /abonelikiptal | var olan **aboneliğinizi iptal eder** ve bot tarafından günlük mesaj almazsınız
- /duyuru | abone olurken kaydolduğunuz bölümünüzün en son yüklenmiş en fazla 12 adet duyurusunu görebilirsiniz. **değer girilmezse son duyuruyu gösterir**
   - `/duyuru 3`
   - `/duyuru`
 </br>
 

![image](https://github.com/bilkodtop/btu-sks-telegram-bot/assets/114951374/36895d20-bffa-4010-a461-9994132eb581)
![image](https://github.com/bilkodtop/btu-sks-telegram-bot/assets/114951374/c883a695-1722-4916-8838-071d5dd56ae9)
![image](https://github.com/bilkodtop/btu-sks-telegram-bot/assets/114951374/a898b756-2ebf-4760-8bb6-6b9250925b8c)


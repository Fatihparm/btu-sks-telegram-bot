import fitz  # PyMuPDF
import re
import os

dosya_dizini = os.path.dirname(os.path.abspath(__file__))
dosya_adi = "pdf0.pdf"
dosya_yolu = os.path.join(dosya_dizini, dosya_adi)

class Menu():
    def __init__(self):
        pass

    def getFormattedMenu(self):
        # Blok verilerini al ve satırları düzenleyerek döndür
        doc = fitz.open(dosya_yolu)
        page = doc.load_page(0)
        blocks = page.get_text("blocks")

        # Blokları birleştirerek tabloyu oluştur
        formatted_menu = []
        temp = ""

        for block in blocks[2:]:  # İlk birkaç blok başlık olabilir, onları atlıyoruz
            text = block[4].strip()

            if re.match(r"\d{2}\.\d{2}\.\d{4}", text):
                if temp:
                    formatted_menu.append(temp.strip())
                    temp = ""
            temp += text + " "  
        if temp:
            formatted_menu.append(temp.strip())
        formatted_menu.pop(0)

        return formatted_menu

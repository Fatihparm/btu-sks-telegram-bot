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
        doc = fitz.open(dosya_yolu)
        page = doc.load_page(0)
        blocks = page.get_text("blocks")

        formatted_menu = []
        temp = []
        collecting = False  # Başlıkları atlamak için flag

        for block in blocks:
            text = block[4].strip()

            # Tarih ile başlayan satırları yakala (ör: 3.2.2025)
            if re.match(r"\d{1,2}\.\d{1,2}\.\d{4}", text):
                if temp:  # Önceki günü listeye ekle
                    formatted_menu.append("\n".join(temp))
                    temp = []
                collecting = True  # Artık menü verilerini topluyoruz

            # Gereksiz başlıkları atlamak için
            if collecting:
                temp.append(text)

        if temp:  # Son günü de ekle
            formatted_menu.append("\n".join(temp))

        return formatted_menu

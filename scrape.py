import requests
from bs4 import BeautifulSoup
from os import path
import hashlib

class ScrapeMenu:
  def __init__(self):
    self.pdf_path = "pdf0.pdf"
    self.hash_path = "pdf_hash.txt"

  def calculate_hash(self, file_path):
    try:
      with open(file_path, 'rb') as f:
        file_hash = hashlib.md5()
        while chunk := f.read(8192):
          file_hash.update(chunk)
      return file_hash.hexdigest()
    except FileNotFoundError:
      print(f"Hata: {file_path} dosyası bulunamadı.")
      return None
    except Exception as e:
      print(f"Hata: Hash hesaplama sırasında bir sorun oluştu: {e}")
      return None

  def get_stored_hash(self):
    if path.exists(self.hash_path):
      try:
        with open(self.hash_path, "r") as f:
          return f.read().strip()
      except Exception as e:
        print(f"Hata: Hash dosyası okunamadı: {e}")
        return None
    return None

  def save_hash(self, new_hash):
    try:
      with open(self.hash_path, "w") as f:
        f.write(new_hash)
      print("Hash kaydedildi.")
    except Exception as e:
      print(f"Hata: Hash dosyası yazılamadı: {e}")

  def is_pdf_updated(self, current_hash):
    stored_hash = self.get_stored_hash()
    if stored_hash is None:
      print("Hash dosyası yok, PDF güncel sayılacak.")
      return True
    if current_hash == stored_hash:
      print("PDF değişmedi.")
      return False
    print("PDF değişti.")
    return True

  def download_pdf(self, url):
    try:
      response = requests.get(url, verify=False, timeout=10)
      response.raise_for_status()
      return response.content
    except requests.RequestException as e:
      print(f"Hata: PDF indirilemedi: {e}")
      return None

  def getPdf(self):
    requests.packages.urllib3.disable_warnings() 
    url = "https://sks.btu.edu.tr/tr/sayfa/detay/4398/beslenme-ve-di̇yeteti̇k"
    try:
      response = requests.get(url, verify=False, timeout=10)
      response.raise_for_status()
      page = BeautifulSoup(response.content, 'html.parser')

      ilan = page.find("table")
      if not ilan:
        print("Hata: Sayfada tablo bulunamadı.")
        return

      trs = ilan.find_all("tr")
      if len(trs) < 2:
        print("Hata: Tabloda yeterli satır yok.")
        return

      link = trs[1].find("a").get("href")
      if not link:
        print("Hata: PDF linki bulunamadı.")
        return

      current_hash = self.calculate_hash(self.pdf_path) if path.exists(self.pdf_path) else None
      pdf_content = self.download_pdf(link)
      if pdf_content is None:
        return
      new_hash = hashlib.md5(pdf_content).hexdigest()
      if current_hash == new_hash:
        print("Mevcut PDF güncel.")
        return
      print("Dosya Indiriliyor")
      with open(self.pdf_path, 'wb') as pdf:
        pdf.write(pdf_content)
      print("PDF Dosyasi Indirildi")
      self.save_hash(new_hash)

    except requests.RequestException as e:
      print(f"Hata: İstek sırasında bir sorun oluştu: {e}")
    except Exception as e:
      print(f"Hata: Beklenmeyen bir sorun oluştu: {e}")

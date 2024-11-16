import requests
from bs4 import BeautifulSoup
from os import path
import hashlib

class ScrapeMenu:

  def __init__(self):
    pass

  def calculate_hash(self, file_path):
    with open(file_path, 'rb') as f:
        file_hash = hashlib.md5()
        while chunk := f.read(8192):
            file_hash.update(chunk)
    return file_hash.hexdigest()

  def is_pdf_updated(self, new_pdf_path):
    old_hash_path = "pdf_hash.txt"

    new_hash = self.calculate_hash(new_pdf_path)

    if path.exists(old_hash_path):
        with open(old_hash_path, "r") as f:
            old_hash = f.read()
        if new_hash == old_hash:
            print("PDF değişmedi.")
            return False

    # pdf has changed
    with open(old_hash_path, "w") as f:
        f.write(new_hash)
    print("PDF değişti.")
    return True

  def getPdf(self):
    requests.packages.urllib3.disable_warnings()
    if path.exists("pdf0.pdf") and not self.is_pdf_updated("pdf0.pdf"):
      print("Mevcut PDF güncel.")
    else:
      url = "https://sks.btu.edu.tr/tr/sayfa/detay/4398/beslenme-ve-di̇yeteti̇k"
      response = requests.get(url, verify=False)
      page = BeautifulSoup(response.content, 'html.parser')
      ilan = page.find("table")
      trs = ilan.find_all("tr")
      link = trs[1].find("a").get("href")
      print("Dosya Indiriliyor")
      response = requests.get(link, verify=False)
      pdf = open("pdf0" + ".pdf", 'wb')
      pdf.write(response.content)
      pdf.close()
      print("PDF Dosyasi Indirildi")

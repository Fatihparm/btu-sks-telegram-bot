from model import Models
import requests
from bs4 import BeautifulSoup
import json
import logging

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s", 
    datefmt="%Y-%m-%d %H:%M:%S", 
    level=logging.INFO  
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger("announcement")
model = Models()

class ScrapeAnnouncement:
  def __init__(self):
    pass
  class Announcement:
    """Duyuru nesnesi. Duyuruları tutmak için kullanılır."""
    def __init__(self, title, link, publish_date):
      self.title = title
      self.link = link
      self.publish_date = publish_date
  
  def getPageContent(self, url):
    """Verilen url adresinden duyuru sayfasını çeker ve duyuruları döndürür."""
    requests.packages.urllib3.disable_warnings()
    response = requests.get(url, verify=False)
    page = BeautifulSoup(response.content, 'html.parser')
    block = page.find("div", class_="ann-list")
    rows = block.find_all("li")
    annList = []
    for row in rows:
      link = row.find("a").get("href")
      publish_date = row.find("span").text
      title = row.find("strong")
      annList.append(self.Announcement(title.text, link, publish_date))
    return annList
   
  def checkForNewAnnouncements(self, lecture):
    old_announcements = model.get_announcement(lecture)
    urls = {ann[3].strip().lower() for ann in old_announcements}  
    with open('lectureUrl.json') as file:
      lecture_url_dict = json.load(file)
    new_announcements = self.getPageContent(lecture_url_dict[lecture])
    new_content = []
    for new_ann in new_announcements:
      normalized_link = new_ann.link.strip().lower()
      if normalized_link not in urls:
        model.add_announcement(new_ann.title, lecture, new_ann.link, new_ann.publish_date)
        new_content.append(new_ann)
    if new_content:
      logger.info(f"{len(new_content)} {lecture.upper()} bölümü duyurusu veritabanına eklendi")
    return new_content[:3] # Spam kontrolü
  
  def getNewAnnouncements(self):
    """Tüm bölümlerin yeni duyurularını bir sözlükte toplar ve döndürür."""
    logger.info("Duyuru kontrolü yapılıyor...")
    new_announcement_dict = {}
    with open('lectureUrl.json') as file:
      lecture_url_dict = json.load(file)
    for lec in lecture_url_dict.keys(): 
      new_announcements = self.checkForNewAnnouncements(lec) 
      if new_announcements: #yeni duyuru varsa sözlüğe ekliyoruz.
        new_announcement_dict[lec] = new_announcements
    return new_announcement_dict
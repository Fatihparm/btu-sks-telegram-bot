from model import Models
import requests
from bs4 import BeautifulSoup
import json

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
   
  def checkForNewAnnouncements(self,lecture):
    """Verilen bölümün duyuru sayfasından yeni duyuruları çeker ve veritabanına ekler. Eklenen duyuruları döndürür."""
    old_announcements = model.get_announcement(lecture) #veritabanındaki duyuruları alıyoruz.
    with open('lectureUrl.json') as file:
      lecture_url_dict = json.load(file)
    new_announcements = self.getPageContent(lecture_url_dict[lecture]) #yeni duyuruları internetten çekiyoruz.
    new_content = []
    urls = []
    counter = 0 
    for ann in old_announcements:
      urls.append(ann[3]) #linkleri listeye ekliyoruz. Yeni duyuruları kontrol ederken bu listeyi kullanacağız.
    for new_ann in new_announcements:
      if new_ann.link not in urls:
        model.add_announcement(new_ann.title, lecture, new_ann.link, new_ann.publish_date) #yeni duyuruyu veritabanına ekliyoruz.
        counter += 1
        new_content.append(new_ann) #yeni duyuruyu listeye ekliyoruz.
    if counter != 0: 
      print(f"{counter} {lecture.upper()} bölümü duyurusu veritabanına eklendi")
    if len(new_content) > 3: # 3'ten fazla duyuru varsa yeni duyuruları döndürmüyoruz. Botun spam yapmasını engellemek için.
      new_content.clear() 
    return new_content
  
  def getNewAnnouncements(self):
    """Tüm bölümlerin yeni duyurularını bir sözlükte toplar ve döndürür."""
    print("Duyuru kontrolü yapılıyor...")
    new_announcement_dict = {}
    with open('lectureUrl.json') as file:
      lecture_url_dict = json.load(file)
    for lec in lecture_url_dict.keys(): 
      new_announcements = self.checkForNewAnnouncements(lec) 
      if new_announcements: #yeni duyuru varsa sözlüğe ekliyoruz.
        new_announcement_dict[lec] = new_announcements
    return new_announcement_dict



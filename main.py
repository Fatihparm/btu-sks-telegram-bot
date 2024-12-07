import getmenu
import scrape
import getannouncement
from model import Models
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackContext
from telegram import Update
import logging
import os
from datetime import time, datetime
import requests
import dotenv
import json

dotenv.load_dotenv()
Token = os.getenv("TOKEN")

models = Models()
models.create_table()

with open("lectureUrl.json", "r", encoding="utf-8") as file:
    data = json.load(file)

lectures = [key for key in data.keys() if key != "sks"]

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s", 
    datefmt="%Y-%m-%d %H:%M:%S", 
    level=logging.INFO  
)

logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger("TelegramBot") 

def log_command(func):
  async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    logger.info(f"{func.__name__} komutu çağrıldı. Kullanıcı: {user.first_name} ({user.id})")
    await func(update, context)
    logger.info(f"{func.__name__} komutu tamamlandı. Kullanıcı: {user.first_name} ({user.id})")
  return wrapper

async def error_handler(update, context):
    print(f"Error: {context.error}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  user = update.message.from_user
  text1 = "Bursa Teknik Üniversitesi Yemekhane Telegram botuna hoşgeldiniz. /help yazarak komutlara erişebilirsiniz.!"
  await context.bot.send_message(chat_id=update.effective_chat.id, text = text1)
  info = update.message
  messages_to_add(info)
  logger.info(f"/start komutu tamamlandı. Kullanıcı: {user.first_name} ({user.id})")

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
  user = update.message.from_user
  print('You talk with user {} and his user ID: {} and his name is {}'.format(
    user['username'], user['id'], user['first_name']))
  reply_text = """/menu <gün> -> girdiğiniz günün menüsünü görebilirsiniz, gün girmezseniz içinde olduğunuz günün menüsünü görebilirsiniz.\n\n/abonelik <bölüm adı> -> botumuzda abonelik başlatarak her gün saat 09.00'da botumuzdan menüyü ve yeni yüklenen sks duyurularını telegram'dan özel mesaj olarak alabilirsiniz. Eğer komutun yanına bölümünüzün adını da yazarsanız yeni eklenen bölüm duyurularını da alırsınız.(Sadece /abonelik yazarak günlük mesaj alamazsınız botun kendisine tıklayıp mesajlaşma başlatmanız gerekmektedir)\n\nGeçerli bölümler:\n\nbilgisayar, biyomuh, cevre, elektrik, endustri,fizik, gida, insaat, kimya, kimyamuh, makine,matematik, mekatronik, metalurji, polimer, denizcilik, utl (tercümanlık), ui (uluslararası ilişkiler), isletme, sosyoloji, imtb, psikoloji, ormanendustri, orman, peyzaj\n\n/duyuru <duyuru sayısı> abone olduğunuz bölümün son eklenen istediğiniz sayıda duyurusunu görebilirsiniz. En fazla 12 duyuru görebilirsiniz.\n\n/abonelikiptal -> aboneliğinizi iptal eder
  """
  await context.bot.send_message(chat_id=update.effective_chat.id, text = reply_text)
  info = update.message
  messages_to_add(info)
  logger.info(f"/help komutu tamamlandı. Kullanıcı: {user.first_name} ({user.id})")


def restartEveryDay(context: CallbackContext):
  global menuList, newAnnDict, sksAnnList
  sksAnnList = []
  logger.info("RESTARTED")
  try:
    scrape.ScrapeMenu().getPdf()
    logger.info("PDF güncellendi")
    menuList = getmenu.Menu().getFormattedMenu()  # Yemekhane menüsünü günceller
    logger.info("Menü güncellendi")
  except Exception as e:
    logger.info(f"PDF güncellenirken bir hata oluştu: {e}")
    menuList = []  # Varsayılan bir boş liste döndürebilirsiniz
  try:
    newAnnDict = getannouncement.ScrapeAnnouncement().getNewAnnouncements()
    logger.info("-----------------------Yeni Duyurular----------------------------")
    for key, announcements in newAnnDict.items():
      logger.info(f"Bölüm: {key}")
      for announcement in announcements:
        logger.info(f"Başlık: {announcement.title}, Tarih: {announcement.publish_date}, Link: {announcement.link}")
  except Exception as e:
    logger.info(f"Duyurular güncellenirken bir hata oluştu: {e}")
    newAnnDict = {}
  try:
    for ann in newAnnDict["sks"]:
      sksAnnList.append(ann) #sks duyurularını ayrıca kaydediyoruz
  except(KeyError):
    logger.info("Sks duyurusu yok")
  if len(newAnnDict) == 0:
    logger.info("Yeni duyuru yok")
  for lecture in lectures:
    models.delete_old_announcements(lecture) #eski duyuruları siler
  models.delete_old_announcements("sks") #sks duyurularını siler
  models.remove_duplicate_announcements() #aynı duyuruları (varsa) siler


async def getMenu(update: Update, context: ContextTypes.DEFAULT_TYPE):
  user = update.message.from_user
  try:
    if context.args == []:
      userInput = datetime.now().day
    else:
      userInput = context.args[0]
    if (int(userInput) > 0):
        daysMenu = menuList[int(userInput)-1]
        lines = daysMenu.split("\n")
        formattedDaysMenu = f"{lines[0]} - {lines[1]}\n" + "\n".join(lines[2:])
        daysMenuText = formattedDaysMenu
        await context.bot.send_message(chat_id=update.effective_chat.id, text = daysMenuText)
  except(IndexError, ValueError):
    await context.bot.send_message(chat_id=update.effective_chat.id, text = "Lütfen geçerli bir gün giriniz.")
  info = update.message
  messages_to_add(info)
  logger.info(f"/menu komutu tamamlandı. Kullanıcı: {user.first_name} ({user.id})")


async def abonelik(update: Update, context: ContextTypes.DEFAULT_TYPE):
  user = update.message.from_user
  first_name = user["first_name"]
  last_name = user["last_name"]
  telegramId = user["id"]
  check_id = models.check_person(telegramId)
  try:  
    if check_id is None:
      if context.args == []:
        models.add_user(telegramId, first_name , last_name, None) #kullanıcı bölümünü girmezse sadece menu sisteminden faydalanabilir.
        text = "Abonelik kaydınız oluşturuldu! Her gün Saat 09:00'da günün menüsü sizinle paylaşılacaktır."
        url = f"https://api.telegram.org/bot{Token}/sendMessage?chat_id={telegramId}&text={text}"
        requests.get(url).json()
        return
      else:
        if context.args[0] not in lectures: #bölüm adı yanlış girildiyse
          text = """Lütfen bölümünüzü giriniz.\n\nbilgisayar, biyomuh, cevre, elektrik, endustri,fizik, gida, insaat, kimya, kimyamuh, makine,matematik, mekatronik, metalurji, polimer,denizcilik, utl (tercümanlık), ui (uluslararası ilişkiler), isletme, sosyoloji, imtb, psikoloji, ormanendustri, orman, peyzaj"""
          url = f"https://api.telegram.org/bot{Token}/sendMessage?chat_id={telegramId}&text={text}"
          requests.get(url).json()
          return
      models.add_user(telegramId, first_name, last_name, context.args[0])
      text = "Abonelik kaydınız oluşturuldu! Her gün Saat 09:00'da günün menüsü ve bölüm duyuru sayfanızdaki yeni duyurular sizinle paylaşılacaktır. /duyuru komutuyla son duyuruları kontrol edebilirsiniz."
      url = f"https://api.telegram.org/bot{Token}/sendMessage?chat_id={telegramId}&text={text}"
      requests.get(url).json()
    else:
      text = "Zaten aboneliğiniz bulunmaktadır. Aboneliğinizi iptal etmek için /abonelikiptal komutunu kullanın."
      url = f"https://api.telegram.org/bot{Token}/sendMessage?chat_id={telegramId}&text={text}"
      requests.get(url).json()
  except Exception as e:
    logger.info(f"Abonelik oluşturulurken bir hata oluştu: {e}")
  info = update.message
  messages_to_add(info)
  logger.info(f"/abonelik komutu tamamlandı. Kullanıcı: {user.first_name} ({user.id}) {context.args[0]}")

async def duyuruBas(update: Update, context: ContextTypes.DEFAULT_TYPE):
  user = update.message.from_user
  telegramId = user["id"]
  check_id = models.check_person(telegramId)
  if check_id is None:
    text = "Aboneliğiniz bulunmamaktadır."
    url = f"https://api.telegram.org/bot{Token}/sendMessage?chat_id={telegramId}&text={text}"
    requests.get(url).json()
    return
  else:
    user_lecture = check_id[3]
    if user_lecture == None:
      text = "Abonelik kaydınızda bölüm adınızı girmemişsiniz. Bu komuttan yararlanmak için önce aboneliğinizi iptal etmeli (/abonelikiptal) sonra aboneliğinizi açarken bölüm adınızı da girmelisiniz (/abonelik <bolum adı>)"
      url = f"https://api.telegram.org/bot{Token}/sendMessage?chat_id={telegramId}&text={text}"
      requests.get(url).json()
      return
    try:
      if context.args == []:
        userInput = 1
      else:
        userInput = int(context.args[0])
      if (int(userInput) > 0 and int(userInput)<13):
          content_list = models.fetch_announcement_by_count(user_lecture, userInput)
          for content in content_list:
            # Tarihi 'YYYY-MM-DD' formatından 'DD.MM.YYYY' formatına çevir
            publish_date = content[4]  # 'publish_date' verisi 'YYYY-MM-DD' formatında
            publish_date_obj = datetime.strptime(publish_date, '%Y-%m-%d')  # strptime doğru şekilde kullanıldı
            formatted_date = publish_date_obj.strftime('%d.%m.%Y')
            text=f"DUYURU \n{formatted_date}\n{content[2]}\n\nDaha fazla bilgi için: {content[3]}"
            url = f"https://api.telegram.org/bot{Token}/sendMessage?chat_id={telegramId}&text={text}"
            requests.get(url).json()
      else:
        url = f"https://api.telegram.org/bot{Token}/sendMessage?chat_id={telegramId}&text=Lütfen geçerli bir sayı (1-12) giriniz."
        requests.get(url).json()
    except Exception as e:
      logger.info(f"Duyuru gönderilirken bir hata oluştu: {e}")
    info = update.message
    messages_to_add(info)
    logger.info(f"/duyuru komutu tamamlandı. Kullanıcı: {user.first_name} ({user.id})")

async def abonelikiptal(update:Update, context:ContextTypes.DEFAULT_TYPE):
  user = update.message.from_user
  telegramId= user["id"]
  check_id = models.check_person(telegramId)
  if check_id is None:
    text = "Aboneliğiniz bulunmamaktadır."
    url = f"https://api.telegram.org/bot{Token}/sendMessage?chat_id={telegramId}&text={text}"
    requests.get(url).json()
  else:
    models.delete_person(telegramId)
    text = "Aboneliğiniz iptal edilmiştir."
    url = f"https://api.telegram.org/bot{Token}/sendMessage?chat_id={telegramId}&text={text}"
    requests.get(url).json()
  info = update.message
  messages_to_add(info)
  logger.info(f"/abonelikiptal komutu tamamlandı. Kullanıcı: {user.first_name} ({user.id})")

def sendSksAnnouncement(context: CallbackContext):
  kayitliKisiListesi = models.check_all()
  for eachPerson in range(len(kayitliKisiListesi)):
    telegramId = kayitliKisiListesi[eachPerson][0]
    try:
      if len(sksAnnList) == 0:
        logger.info("Yeni sks duyurusu yok")
        break
      for content in sksAnnList:
        text=f"DUYURU\n{content.title}\n{content.publish_date}\n\nDaha fazla bilgi için:{content.link})"
        url = f"https://api.telegram.org/bot{Token}/sendMessage?chat_id={telegramId}&text={text}"
        requests.get(url).json()
    except Exception as e:
      logger.info(f"{telegramId} kullanıcısında hata oluştu: {e}")
      eachPerson += 1

def sendAnnouncement(context: CallbackContext):
  kayitliKisiListesi = models.check_all()
  for eachPerson in range(len(kayitliKisiListesi)):
    telegramId = kayitliKisiListesi[eachPerson][0]
    user_lecture = kayitliKisiListesi[eachPerson][3]
    logger.info("Bolum: " + user_lecture)
    if user_lecture == None:
      logger.info("Kullanicinin bolumu yok")
      break
    if len(newAnnDict) == 0:
      logger.info("Yeni duyuru yok")
      break
    try:
      for content in newAnnDict[user_lecture]:
        text=f"DUYURU \n{content.title.upper()}\n{content.publish_date}\n\nDaha fazla bilgi için:{content.link}"
        url = f"https://api.telegram.org/bot{Token}/sendMessage?chat_id={telegramId}&text={text}"
        requests.get(url).json()
    except Exception as e:
      logger.info(f"{telegramId} kullanıcısında hata oluştu: {e}")
      eachPerson += 1

def sendDaysMenu(context: CallbackContext):
  kayitliKisiListesi = models.check_all()
  userInput = datetime.now().day
  daysMenu = menuList[int(userInput)-1]
  lines = daysMenu.split("\n")
  formattedDaysMenu = f"{lines[0]} - {lines[1]}\n" + "\n".join(lines[2:])
  for eachPerson in range(len(kayitliKisiListesi)):
    telegramId = kayitliKisiListesi[eachPerson][0]
    try:
      url = f"https://api.telegram.org/bot{Token}/sendMessage?chat_id={telegramId}&text={formattedDaysMenu}"
      requests.get(url).json()
    except Exception as e:
      logger.info(f"{telegramId} kullanıcısında hata oluştu: {e}")
      eachPerson += 1

def messages_to_add(info):
  user = info.from_user
  first_name = user["first_name"]
  last_name = user["last_name"]
  telegramId = user["id"]
  message = info.text
  models.add_message(telegramId, first_name, last_name, message)

"""BURADAN TÜM FONKSİYONLARIN ÇALIŞMA SAATLERİNİ AYARLAYABİLİRSİNİZ (hour değişkenini 3 saat geriden almalısınız)."""

def callbackRestartEveryday(context: ContextTypes.DEFAULT_TYPE):
  timer = time(hour=5, minute=0, second=0)
  context.job_queue.run_daily(restartEveryDay, timer, days=(0,1,2,3,4,5,6))
  timer2 = time(hour=8, minute=0, second=0)
  context.job_queue.run_daily(restartEveryDay, timer2, days=(0,1,2,3,4,5,6))
  timer3 = time(hour=16, minute=0, second=0)
  context.job_queue.run_daily(restartEveryDay, timer3, days=(0,1,2,3,4,5,6))

def callbackMenu(context: ContextTypes.DEFAULT_TYPE):
  timer = time(hour=6, minute=0, second=0)
  context.job_queue.run_daily(sendDaysMenu, timer, days=(0,1,2,3,4,5,6))

def callbackAnnouncement(context: ContextTypes.DEFAULT_TYPE):
  timer = time(hour=7, minute=0, second=0)
  context.job_queue.run_daily(sendAnnouncement, timer, days=(0,1,2,3,4,5,6))
  timer2 = time(hour=16, minute=0, second=0)
  context.job_queue.run_daily(restartEveryDay, timer2, days=(0,1,2,3,4,5,6))

def callbackSksAnnouncement(context: ContextTypes.DEFAULT_TYPE):
  timer = time(hour=7, minute=0, second=0)
  context.job_queue.run_daily(sendSksAnnouncement, timer, days=(0,1,2,3,4,5,6))
  timer2 = time(hour=16, minute=0, second=0)
  context.job_queue.run_daily(restartEveryDay, timer2, days=(0,1,2,3,4,5,6))

def main():
  app = ApplicationBuilder().token(Token).build()
  app.add_handler(CommandHandler("start", start))
  app.add_handler(CommandHandler('help',help))
  app.add_handler(CommandHandler('menu',getMenu))
  app.add_handler(CommandHandler('abonelik',abonelik))
  app.add_handler(CommandHandler('abonelikiptal',abonelikiptal))
  app.add_handler(CommandHandler('duyuru',duyuruBas))
  app.add_error_handler(error_handler)
  restartEveryDay(app)
  callbackRestartEveryday(app)
  callbackMenu(app)
  callbackAnnouncement(app)
  callbackSksAnnouncement(app)
  app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
  main()
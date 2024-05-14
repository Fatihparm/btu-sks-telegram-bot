import sqlite3
from dotenv import load_dotenv
import os

load_dotenv()
Token = os.getenv("TOKEN")
class Models:

  def __init__(self):
    self.db = sqlite3.connect('database.db', check_same_thread=False)
    self.cursor = self.db.cursor()
    self.create_table()

  def create_table(self):
    """Creates table if not exists"""
    self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS subscriptions (
            chat_id TEXT PRIMARY KEY NOT NULL, 
            first_name TEXT DEFAULT "",
            last_name TEXT DEFAULT "",
            lecture TEXT DEFAULT "",
            subsdate DATETIME DEFAULT CURRENT_TIMESTAMP
            )    
        ''')
    self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY,
            chat_id TEXT NOT NULL, 
            first_name TEXT DEFAULT "",
            last_name TEXT DEFAULT "",
            message TEXT DEFAULT "",
            message_date DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
    self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS announcements (
            id INTEGER PRIMARY KEY,
            lecture TEXT DEFAULT "",
            title TEXT DEFAULT "",
            link TEXT DEFAULT "",
            publish_date DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
    self.db.commit()


  def add_user(self, chat_id, first_name, last_name, lecture):
    """Adds people to database"""
    self.cursor.execute(
      '''
        INSERT INTO subscriptions (chat_id, first_name, last_name, lecture) VALUES (?, ?, ?, ?)
        ''', (chat_id, first_name, last_name, lecture))
    self.db.commit()

  def delete_person(self, chat_id):
    """Deletes people from database"""
    self.cursor.execute(
      '''
        DELETE FROM subscriptions WHERE chat_id = ?
        ''', (chat_id, ))
    self.db.commit()

  def check_person(self, chat_id):
    """Checks if people exists"""
    self.cursor.execute(
      '''
        SELECT * FROM subscriptions WHERE chat_id = ?
        ''', (chat_id, ))
    return self.cursor.fetchone()

  def check_all(self):
    self.cursor.execute('''
        SELECT * FROM subscriptions 
        ''')
    return self.cursor.fetchall()
  
  def add_message(self, chat_id, first_name, last_name, message):
    self.cursor.execute(
      "INSERT INTO messages (chat_id, first_name, last_name,message) VALUES (?, ?, ?, ?)",
      (chat_id, first_name, last_name, message))
    self.db.commit()

  def get_all_messages(self):
    self.cursor.execute('''
        SELECT * FROM messages
        ''')
    return self.cursor.fetchall()

  def add_announcement(self,title, lecture, link,publish_date):
    """Adds lecture announcements to database"""
    self.cursor.execute(
      '''
        INSERT INTO announcements (title, lecture, link,publish_date) VALUES (?, ?, ?, ?)
        ''', (title, lecture, link,publish_date))
    self.db.commit()

  def remove_duplicate_announcements(self):
    self.cursor.execute('''
        DELETE FROM announcements WHERE id NOT IN (SELECT MIN(id) FROM announcements GROUP BY link)
        ''')
    self.db.commit()
  
  def delete_announcement(self,id):
    """Deletes announcements from database"""
    self.cursor.execute(
      '''
        DELETE FROM announcements WHERE id = ?
        ''', (id,))
    self.db.commit()

  def check_all_announcements(self):
    self.cursor.execute('''
        SELECT id,title FROM announcements
        ''')
    return self.cursor.fetchall()
  
  def get_all_announcement(self):
      self.cursor.execute('''
        SELECT * FROM announcements
        ''')
      return self.cursor.fetchall()
  
  def get_announcement(self, lecture):
      self.cursor.execute('''
        SELECT * FROM announcements WHERE lecture = ?
        ''',(lecture,))
      return self.cursor.fetchall()
  
  def fetch_announcement_by_count(self, lecture, count):
      self.cursor.execute('''
        SELECT * FROM announcements WHERE lecture = ? ORDER BY strftime('%d-%m-%Y', publish_date) DESC LIMIT ?
        ''',(lecture,count))
      return self.cursor.fetchall()


s = Models()
s.create_table()
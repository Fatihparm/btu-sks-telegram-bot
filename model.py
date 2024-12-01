import sqlite3
from dotenv import load_dotenv
import os

load_dotenv()
Token = os.getenv("TOKEN")
class Models:

  def __init__(self):
    self.db = sqlite3.connect('./data/database.db', check_same_thread=False)
    self.cursor = self.db.cursor()
    self.create_table()

  def create_table(self):
    """Creates tables if not exist"""
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
    """Adds a user to the database"""
    self.cursor.execute(
      '''
      INSERT OR IGNORE INTO subscriptions (chat_id, first_name, last_name, lecture) 
      VALUES (?, ?, ?, ?)
      ''', (chat_id, first_name, last_name, lecture))
    self.db.commit()

  def delete_person(self, chat_id):
    """Deletes a user from the database"""
    self.cursor.execute(
      '''
      DELETE FROM subscriptions WHERE chat_id = ?
      ''', (chat_id,))
    self.db.commit()

  def check_person(self, chat_id):
    """Checks if a user exists"""
    self.cursor.execute(
      '''
      SELECT * FROM subscriptions WHERE chat_id = ?
      ''', (chat_id,))
    return self.cursor.fetchone()

  def check_all(self):
    """Fetches all users"""
    self.cursor.execute('''
      SELECT * FROM subscriptions 
      ''')
    return self.cursor.fetchall()

  def add_message(self, chat_id, first_name, last_name, message):
    """Adds a message to the database"""
    self.cursor.execute(
      '''
      INSERT INTO messages (chat_id, first_name, last_name, message) 
      VALUES (?, ?, ?, ?)
      ''', (chat_id, first_name, last_name, message))
    self.db.commit()

  def get_all_messages(self):
    """Fetches all messages"""
    self.cursor.execute('''
      SELECT * FROM messages
      ''')
    return self.cursor.fetchall()

  def add_announcement(self, title, lecture, link, publish_date):
    """Adds an announcement to the database"""
    formatted_date = self.format_date(publish_date)
    self.cursor.execute(
      '''
      INSERT INTO announcements (title, lecture, link, publish_date) 
      VALUES (?, ?, ?, ?)
      ''', (title, lecture, link, formatted_date))
    self.db.commit()

  def remove_duplicate_announcements(self):
    """Removes duplicate announcements based on link"""
    self.cursor.execute('''
      DELETE FROM announcements 
      WHERE id NOT IN (
        SELECT MIN(id) 
        FROM announcements 
        GROUP BY link
      )
    ''')
    self.db.commit()

  def delete_announcement(self, id):
    """Deletes an announcement by ID"""
    self.cursor.execute(
      '''
      DELETE FROM announcements WHERE id = ?
      ''', (id,))
    self.db.commit()

  def delete_old_announcements(self, lecture):
    """Keeps only the latest 12 announcements for a lecture"""
    self.cursor.execute("SELECT COUNT(*) FROM announcements WHERE lecture = ?", (lecture,))
    total_count = self.cursor.fetchone()[0]
    if (total_count > 12):
      self.cursor.execute('''
        DELETE FROM announcements
        WHERE id IN (
          SELECT id 
          FROM announcements
          WHERE lecture = ?
          ORDER BY publish_date ASC
          LIMIT ?
        )
      ''', (lecture, total_count - 12))
      self.db.commit()

  def check_all_announcements(self):
    """Fetches all announcement titles and IDs"""
    self.cursor.execute('''
      SELECT id, title FROM announcements
      ''')
    return self.cursor.fetchall()

  def get_all_announcements(self):
    """Fetches all announcements"""
    self.cursor.execute('''
      SELECT * FROM announcements
      ''')
    return self.cursor.fetchall()

  def get_announcement(self, lecture):
    """Fetches all announcements for a specific lecture"""
    self.cursor.execute('''
      SELECT * FROM announcements WHERE lecture = ?
      ''', (lecture,))
    return self.cursor.fetchall()

  def fetch_announcement_by_count(self, lecture, count):
    """Fetches the latest `count` announcements for a lecture"""
    self.cursor.execute('''
      SELECT * FROM announcements 
      WHERE lecture = ? 
      ORDER BY publish_date DESC 
      LIMIT ?
      ''', (lecture, count))
    return self.cursor.fetchall()

  def format_date(self, date_str):
    """Converts date from DD.MM.YYYY to YYYY-MM-DD format"""
    day, month, year = date_str.split(".")
    return f"{year}-{month}-{day}"

s = Models()
s.create_table()
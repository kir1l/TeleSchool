import sqlite3
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, db_name: str = 'bot_database.db'):
        self.db_name = db_name
        logger.info(f"Database initialized with name: {self.db_name}")

    def get_connection(self):
        try:
            conn = sqlite3.connect(self.db_name)
            conn.row_factory = sqlite3.Row
            logger.info(f"Connection to database {self.db_name} established")
            return conn
        except sqlite3.Error as e:
            logger.error(f"Error connecting to database {self.db_name}: {e}")
            return False

    def init_db(self):
        try:
            with self.get_connection() as conn:
                conn.execute('''CREATE TABLE IF NOT EXISTS users
                                (user_id INTEGER PRIMARY KEY, 
                                notifications_enabled INTEGER DEFAULT 1)''')
            logger.info("Database initialized successfully")
        except sqlite3.Error as e:
            logger.error(f"Error initializing database: {e}")
            return False

    def add_user(self, user_id: int):
        try:
            with self.get_connection() as conn:
                conn.execute('INSERT OR IGNORE INTO users (user_id) VALUES (?)', (user_id,))
            logger.info(f"User {user_id} added to database")
            return True
        except:
            logger.error(f"Error adding user {user_id} to database: {e}")
            return False

    def get_active_users(self) -> List[Dict]:
        try:
            with self.get_connection() as conn:
                users = [dict(row) for row in conn.execute('SELECT user_id FROM users WHERE notifications_enabled = 1')]
            logger.info(f"Retrieved {len(users)} active users")
            return users
        except sqlite3.Error as e:
            logger.error(f"Error retrieving active users: {e}")
            return []

    def toggle_notifications(self, user_id: int, status: int):
        try:
            with self.get_connection() as conn:
                conn.execute('UPDATE users SET notifications_enabled = ? WHERE user_id = ?', (status, user_id))
            logger.info(f"Notifications toggled to {status} for user {user_id}")
        except sqlite3.Error as e:
            logger.error(f"Error toggling notifications for user {user_id}: {e}")
            return False

    def get_user_notification_status(self, user_id: int) -> bool:
        try:
            with self.get_connection() as conn:
                result = conn.execute('SELECT notifications_enabled FROM users WHERE user_id = ?', (user_id,)).fetchone()
            status = bool(result['notifications_enabled']) if result else False
            logger.info(f"Notification status for user {user_id}: {status}")
            return status
        except sqlite3.Error as e:
            logger.error(f"Error getting notification status for user {user_id}: {e}")
            return False

db = Database('bot_database.db')

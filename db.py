import sqlite3

def init_db():
    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, first_name TEXT, last_name TEXT, channel1 INTEGER, channel2 INTEGER, channel3 INTEGER)")
    conn.commit()
    conn.close()

def save_user_data(user_id, user_data):
    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (id, username, first_name, last_name) VALUES (?, ?, ?, ?)", (user_id, user_data['username'], user_data['first_name'], user_data['last_name']))
    conn.commit()
    conn.close()

def update_user_subscription(user_id, chat_id, is_subscribed):
    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()
    if chat_id == "https://t.me/vchempower":
        cursor.execute("UPDATE users SET channel1 = ? WHERE id = ?", (is_subscribed, user_id))
    conn.commit()
    conn.close()
    
def get_user_subscriptions(user_id):
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()

    cursor.execute("SELECT channel1 FROM users WHERE id=?", (user_id,))
    result = cursor.fetchone()

    conn.close()

    return {'channel1': result[0]}


def get_user_subscription(user_id):
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    cursor.execute("SELECT channel1 FROM users WHERE id=?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    if result is not None:
        return result[0]
    else:
        return 0


def get_all_user_ids():
    with sqlite3.connect('bot.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users")
        return [row[0] for row in cursor.fetchall()]       
        
def get_all_user_data():
    with sqlite3.connect('bot.db') as conn:
        conn.row_factory = sqlite3.Row
        with conn:
            result = conn.execute("SELECT * FROM users")
            return [dict(row) for row in result.fetchall()]

def get_total_users():
    with sqlite3.connect('bot.db') as conn:
        cursor = conn.cursor()
        total_users = cursor.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        return total_users
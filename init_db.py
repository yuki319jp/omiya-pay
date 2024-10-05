import sqlite3

# SQLiteデータベースの初期化
def init_db():
    conn = sqlite3.connect('omiyapay.db')
    cursor = conn.cursor()
    
    # ユーザーテーブルの作成
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        balance REAL DEFAULT 0
    )
    ''')
    
    # 初期ユーザーの作成（必要に応じて）
    cursor.execute("INSERT OR IGNORE INTO users (username, password, balance) VALUES (?, ?, ?)", 
                   ('admin', 'admin_password_hash', 1000))  # ここにハッシュ化したパスワードを入力

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()

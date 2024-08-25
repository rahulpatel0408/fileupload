import sqlite3

DATABASE = 'database.db'  


def create_users_table():
    try:
        conn = sqlite3.connect(DATABASE)
        conn.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL
            )
        ''')
        conn.commit()
    except Exception as e:
        print(f"Error creating Table: {e}")
  
def show_table():
    conn = sqlite3.connect(DATABASE)
    try:
        users = conn.execute("SELECT * FROM users").fetchall()
        print(users)
    except Exception as e:
        print(f"Unable to show table: {e}")
        
def add_user():
    username = input("Enter username: ")
    password = input("Enter password: ")
    role = input("Enter role: ")
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()


    try:
        cursor.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', 
                       (username, password, role))
        conn.commit()
        print(f"User '{username}' added successfully with role '{role}'.")
    except sqlite3.IntegrityError:
        print(f"Error: User '{username}' already exists.")
    finally:
        conn.close()

if __name__ == '__main__':
    add_user()
    show_table()
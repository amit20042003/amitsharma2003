import sqlite3

def create_db():
    con = sqlite3.connect(database=r'ims.db')
    cur = con.cursor()

    # Create employee table
    cur.execute("CREATE TABLE IF NOT EXISTS employee(eid INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, gender TEXT, contact TEXT, dob TEXT, doj TEXT, pass TEXT, utype TEXT, address TEXT, salary TEXT)")
    con.commit()

    # Create supplier table
    cur.execute("CREATE TABLE IF NOT EXISTS supplier(invoice INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, contact TEXT, desc TEXT)")
    con.commit()

    # Create category table
    cur.execute("CREATE TABLE IF NOT EXISTS category(cid INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)")
    con.commit()

    # Create product table
    cur.execute("CREATE TABLE IF NOT EXISTS product(pid INTEGER PRIMARY KEY AUTOINCREMENT, Category TEXT, Supplier TEXT, name TEXT, price TEXT, qty TEXT, status TEXT)")
    con.commit()

    # Create payments table (if not exists)
    cur.execute('''
    CREATE TABLE IF NOT EXISTS payments (
        payment_id INTEGER PRIMARY KEY,
        bill_id INTEGER,
        amount_paid REAL,
        payment_date TEXT,
        remaining_balance REAL,
        payment_type TEXT,
        due_date TEXT
    );
    ''')
    con.commit()

    print("Database tables are set up successfully!")

# Call the function to create the database and tables
create_db()

import sqlite3


base = sqlite3.connect("data.db")
cur = base.cursor()

base.execute("""
            CREATE TABLE IF NOT EXISTS Currencies (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Code TEXT UNIQUE,
            FullName TEXT,
            Sign TEXT
            )
            """
            )

base.commit()

currency_data = {"USD": ("USD", "United States dollar", "$"),
                    "AUD": ("AUD", "Australian dollar", "A$")
                     }

# for currency in currency_data:
#     try:
#         cur.execute("INSERT INTO Currencies (Code, FullName, Sign) VALUES(?, ?, ?)", currency_data[currency])
#         base.commit()
#     except sqlite3.IntegrityError as e:
#         print(f"Валюта с таким кодом '{currency_data[currency][0]}' уже существует - 409")

r = cur.execute("SELECT FullName FROM Currencies WHERE Code == ?", ('USD',)).fetchone()

print(r)

cur.close()

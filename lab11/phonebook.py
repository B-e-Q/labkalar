import psycopg2 as psg
import csv




conn = psg.connect(host="localhost", dbname="phonebook", user="postgres", password="Aa12340987.", port=5432)

cur = conn.cursor()

# Create Table
cur.execute(""" CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            surname VARCHAR(50) NOT NULL,
            phone VARCHAR(15) NOT NULL
);
""")


#1 search by pattern
def search(pattern):
    cur.execute("""
        SELECT id, first_name, surname, phone
        FROM phonebook
        WHERE first_name ILIKE %s
           OR surname ILIKE %s
           OR phone ILIKE %s;
    """, (pattern, pattern, pattern))
    res = cur.fetchall()
    for row in res:
        print(row)

search("Nurasyl")


#2 insert name and phone if name exists in table update phone
name = input("enter your name: ")
new_phone = input("enter new phone: ")

cur.execute("SELECT 1 FROM phonebook WHERE first_name = %s", (name,))
exists = cur.fetchone()

if exists:
    cur.execute("UPDATE phonebook SET phone = %s WHERE first_name = %s", (new_phone, name))
else:
    cur.execute("INSERT INTO phonebook (first_name, surname, phone) VALUES (%s, %s, %s)", (name, "a", new_phone))



#3 inserting from list with loop
lst = [
    ["Alice", "Brown", "+1234567890"],
    ["Bob", "Smith", "+23582323457"],
    ["Eve", "White", "+2347867834"]
]

for user in lst:
    cur.execute("INSERT INTO phonebook (first_name, surname, phone) VALUES (%s, %s, %s)", (user[0], user[1], user[2]))



#4 Quering by limit and offset

def pagin(limit, offset):
    cur.execute(""" 
        SELECT id, first_name, surname, phone
        FROM phonebook
        ORDER BY id
        LIMIT %s OFFSET %s
    """, (limit, offset))
    rows = cur.fetchall()
    for row in rows:
        print(row)

pagin(3, 3)

#5 deleting from table
def delete(name = None, phone = None):
    if name:
        cur.execute("DELETE FROM phonebook WHERE first_name = %s", (name,))
    elif phone:
        cur.execute("DELETE FROM phonebook WHERE phone = %s", (phone,))


delete(name="bek")

conn.commit()

cur.close()
conn.close()
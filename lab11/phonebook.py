import psycopg2 as psg

""""
CREATE OR REPLACE FUNCTION search_by_pattern(pattern VARCHAR)
RETURNS TABLE(id int, first_name VARCHAR, surname VARCHAR, phone VARCHAR) AS
$$
BEGIN
    RETURN QUERY
    SELECT phonebook.id, phonebook.first_name, phonebook.surname, phonebook.phone
    FROM phonebook
    WHERE phonebook.first_name ILIKE '%' || pattern || '%'
    OR phonebook.surname ILIKE '%' || pattern || '%'
    OR phonebook.phone ILIKE '%' || pattern || '%';
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE insert_element(name VARCHAR, new_phone VARCHAR) AS
$$
BEGIN
    UPDATE phonebook SET phone = new_phone WHERE first_name = name;
    IF NOT FOUND THEN
        INSERT INTO phonebook (first_name, surname,  phone)
        VALUES (name, 'a', new_phone);
    END IF;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE insert_lst(name VARCHAR, surname VARCHAR, phone VARCHAR) AS
$$
BEGIN 
    INSERT INTO phonebook (first_name, surname, phone)
        VALUES (name, surname, phone);
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION querys(a INT, b INT)
RETURNS TABLE(id int, first_name VARCHAR, surname VARCHAR, phone VARCHAR) AS
$$
BEGIN
    RETURN QUERY
    SELECT phonebook.id, phonebook.first_name, phonebook.surname, phonebook.phone
    FROM phonebook
    ORDER BY phonebook.id
    LIMIT a OFFSET b;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE delete_by(name VARCHAR, userphone VARCHAR) AS
$$
BEGIN 
    DELETE FROM phonebook
    WHERE first_name = name;

    IF NOT FOUND THEN
        DELETE FROM phonebook
        WHERE phonebook.phone = userphone;
    END IF;
END;
$$ LANGUAGE plpgsql;

"""


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
    cur.callproc('search_by_pattern', (pattern,))
    res = cur.fetchall()
    for row in res:
        print(row)

search("Nurasyl")


#2 insert name and phone if name exists in table update phone
def insert(name, new_phone):
    cur.execute("CALL insert_element(%s, %s)", (name, new_phone,))

insert('bew', '1234097532')



#3 inserting from list with loop
lst = [
    ["Alice", "Brown", "+1234567890"],
    ["Bob", "Smith", "+23582323457"],
    ["Eve", "White", "+2347867834"]
]

for user in lst:
    cur.execute("CALL insert_lst(%s, %s, %s)", (user[0], user[1], user[2]))



#4 Quering by limit and offset

def pagin(limit, offset):
    cur.callproc('querys', (limit, offset))
    rows = cur.fetchall()
    for row in rows:
        print(row)

pagin(3, 3)

#5 deleting from table
def delete(name = None, phone = None):
    cur.execute("CALL delete_by(%s, %s)", (name, phone))


delete(name="bek")

conn.commit()

cur.close()
conn.close()
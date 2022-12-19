import sqlite3
import csv

def createSupplierTable():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    with conn:
        c.execute('''CREATE TABLE IF NOT EXISTS SUPPLIER
                    (Email TEXT NOT NULL,
                    Fname  TEXT NOT NULL,
                    LName  TEXT NOT NULL,
                    Phone_Number INTEGER,
                    Longitude INTEGER NOT NULL,
                    Latitude INTEGER NOT NULL,
                    PRIMARY KEY (Email));''')
    conn.close()

def insertFromCsv(fileName):
    conn = sqlite3.connect("Gas_Station.db")
    with open(fileName, newline='') as csvfile:
        spamreader = csv.DictReader(csvfile)
        for tuple in spamreader:
            insertInto(tuple['Email'], tuple['Fname'],
                        tuple['Lname'], tuple['Phone_Number'], tuple['Longitude'],
                        tuple['Latitude'], conn)
    conn.close()

def insertInto(email, fname, lname, phone_number, longitude, latitude, conn=False):
    if (conn == False):
        conn = sqlite3.connect("Gas_Station.db")
        c = conn.cursor()
        with conn:
            try:
                c.execute('''INSERT INTO SUPPLIER
                            VALUES (?,?,?,?,?,?);''', (email, fname,
                            lname, phone_number, longitude,
                            latitude))
            except Exception:
                pass # tuple already added
        conn.close()
    else:
        c = conn.cursor()
        with conn:
            try:
                c.execute('''INSERT INTO SUPPLIER
                            VALUES (?,?,?,?,?,?);''', (email, fname,
                            lname, phone_number, longitude,
                            latitude))
            except Exception:
                pass

def searchByName():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    c.execute("select Fname from SUPPLIER")
    data = c.fetchall()
    conn.close()
    return data
import sqlite3
import csv
import pandas as pd

df = pd.read_csv("Datasets/contract.csv")
li = []
for date in df['Start_Date']:
    numbers = date.split('/')
    if (len(numbers[0]) == 1):
        if (len(numbers[1]) == 1):
            day = '0' + numbers[0]
            month = '0' + numbers[1]
        else:
            day = '0' + numbers[0]
            month = numbers[1]
    else:
        if (len(numbers[1]) == 1):
            day = numbers[0]
            month = '0' + numbers[1]
        else:
            day = numbers[0]
            month = numbers[1]
    correct_date = '/'.join([day, month, numbers[2]])
    li.append(correct_date)
df['Start_Date'] = li

li = []
for date in df['End_Date']:
    numbers = date.split('/')
    if (len(numbers[0]) == 1):
        if (len(numbers[1]) == 1):
            day = '0' + numbers[0]
            month = '0' + numbers[1]
        else:
            day = '0' + numbers[0]
            month = numbers[1]
    else:
        if (len(numbers[1]) == 1):
            day = numbers[0]
            month = '0' + numbers[1]
        else:
            day = numbers[0]
            month = numbers[1]
    correct_date = '/'.join([day, month, numbers[2]])
    li.append(correct_date)
df['End_Date'] = li
df.to_csv("Datasets/contract.csv", index=False)


def createContractTable():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    with conn:
        try:
            c.execute('''CREATE TABLE CONTRACT
                        (Id             INTEGER     NOT NULL,
                        Start_Date      TEXT        NOT NULL,
                        End_Date        TEXT        NOT NULL,
                        Salary          REAL        NOT NULL,
                        PRIMARY KEY (Id))
                        ;''')
            insertFromCsv("Datasets/contract.csv")
        except Exception as e:
            pass  # Database created
    conn.close()


def insertFromCsv(fileName):
    conn = sqlite3.connect("Gas_Station.db")
    with open(fileName, newline='', encoding='utf_8_sig') as csvfile:
        spamreader = csv.DictReader(csvfile)
        for tuple in spamreader:
            insertInto(tuple['id'], tuple['Start_Date'],
                       tuple['End_Date'], tuple['Salary'], conn)
    conn.close()


def insertInto(id, start_date, end_date, salary, conn=False):
    if (conn == False):
        conn = sqlite3.connect("Gas_Station.db")
        c = conn.cursor()
        with conn:
            try:
                c.execute('''INSERT INTO CONTRACT
                            VALUES (?,?,?,?);''', (id, start_date,
                                                   end_date, salary))
            except Exception as e:
                pass  # tuple already added
        conn.close()
    else:
        c = conn.cursor()
        with conn:
            try:
                c.execute('''INSERT INTO CONTRACT
                            VALUES (?,?,?,?);''', (id, start_date,
                                                   end_date, salary))
            except Exception as e:
                pass


def searchBy(id, start_date, end_date, salary):
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    with conn:
        if (id):
            c.execute('''
                        SELECT * 
                        FROM CONTRACT
                        WHERE Id = ?''',
                      (id, ))
        elif (start_date):
            if (end_date):
                if (salary):
                    c.execute('''
                        SELECT * 
                        FROM CONTRACT
                        WHERE Start_Date = ? AND End_Date = ?
                        AND Salary = ?''',
                              (start_date, end_date, salary))
                else:
                    c.execute('''
                        SELECT * 
                        FROM CONTRACT
                        WHERE Start_Date = ? AND End_Date = ?''',
                              (start_date, end_date))
            elif (salary):
                c.execute('''
                        SELECT * 
                        FROM CONTRACT
                        WHERE Start_Date = ? AND Salary = ?''',
                          (start_date, salary))
            else:
                c.execute('''
                        SELECT * 
                        FROM CONTRACT
                        WHERE Start_Date = ?''',
                          (start_date, ))
        elif (end_date):
            if (salary):
                c.execute('''
                        SELECT * 
                        FROM CONTRACT
                        WHERE End_Date = ? AND Salary = ?''',
                          (end_date, salary))
            else:
                c.execute('''
                        SELECT * 
                        FROM CONTRACT
                        WHERE End_Date = ?''',
                          (end_date, ))
        else:
            c.execute('''
                        SELECT * 
                        FROM CONTRACT
                        WHERE Salary = ?''',
                      (salary, ))

    data = c.fetchall()
    conn.close()
    return data


def update(id, start_date, end_date, salary):
    conn = sqlite3.connect("Gas_Station.db")
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()
    with conn:
        try:
            c.execute('''UPDATE CONTRACT
                        SET Start_Date = ?, End_Date = ?, Salary = ?
                        WHERE Id = ?''',
                      (start_date, end_date, salary, id))
        except Exception as e:
            print("Update exception")
            print(e)
    conn.close()


def delete(id):
    conn = sqlite3.connect("Gas_Station.db")
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()
    with conn:
        try:
            c.execute('''DELETE FROM
                        CONTRACT WHERE
                        Id = ?''', (id,))
        except Exception as e:
            print(e)
    conn.close()


def retrieveAllColumns():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    c.execute("select * from CONTRACT")
    data = c.fetchall()
    conn.close()
    return data


def allContractIds():
    conn = sqlite3.connect("Gas_Station.db")
    c = conn.cursor()
    c.execute("select Id from CONTRACT")
    data = c.fetchall()
    conn.close()
    return data

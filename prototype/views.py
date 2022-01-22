import sqlite3
from flask import Flask
from flask import render_template
from . import app

import os

@app.route("/")
def home():
    return render_template('home.html')


@app.route("/scholarship")
def scholarship():
    """
    if os.path.isfile("scholarship_database.db"):
        con = sqlite3.connect("scholarship_database.db")

    con.row_factory = sqlite3.Row
    cur = con.cursor()

    #write query
    query = "select * from scholarship where type = ?"

    #execute queries and get rows
    cur.execute(query)
    rows = cur.fetchall() 

    cur.close()
    """

    return render_template('scholarship_search.html')#, rows = rows)

@app.route("/bursary")
def bursary():
    """
    con = sqlite3.connect("prototype/bursary_database.db")

    con.row_factory = sqlite3.Row
    cur = con.cursor()

    #write query and filter
    query = "select * from bursary where type = ?"

    #execute queries and get rows
    cur.execute(query)
    rows = cur.fetchall() 

    cur.close()

    #Debug
    for r in rows:
        print(r[0])
    """

    return render_template('bursary_search.html')#, rows = rows)




#Debugging
#Print all from database to terminal
@app.route("/list_bursary")
def list():
    if os.path.isfile("prototype/bursary_database.db"):
        con = sqlite3.connect("prototype/bursary_database.db")

    con.row_factory = sqlite3.Row
    cur = con.cursor()

    cur.execute("select * from bursary")
    rows = cur.fetchall()
    print(len(rows))
    for r in rows:
        print(r[0])

    return "Rows returned. Check terminal"

#Print all from database to terminal
@app.route("/list_scholarship")
def list_s():
    if os.path.isfile("prototype/scholarship_database.db"):
        con = sqlite3.connect("prototype/scholarship_database.db")

    con.row_factory = sqlite3.Row
    cur = con.cursor()

    cur.execute("select * from scholarship")
    rows = cur.fetchall()
    print(len(rows))
    for r in rows:
        print(r[0])

    return "Rows returned. Check terminal"
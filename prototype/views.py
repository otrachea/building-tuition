from re import template
import sqlite3
from typing import final
from flask import Flask, request
from flask import render_template
from . import app

import os

@app.route("/")
def home():
    return render_template('home.html')

@app.route('/filter_results', methods = ['POST', 'GET'])
def filter_results():
    return "Filter"

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

#CHANGE
@app.route("/search_template")
def search_template():
    options = load_scholarship_options()
    #fetch everything from database
    return render_template('search-template.html',aoss=options[0],institutions=options[1], genders=options[2], nationalities=options[3], degree_types=options[4])

#FILTER OPTIONS
def filter_scholarship():
    #if request.method == 'POST':
        #Get everything that should be filtered by
        #area of study, institution, gender, nationality, degree type
        #aos = request.form.get('area-of-study-filter')
        
        aos = "Politics"
        institution = ""
        gender = ""
        nationality = ""
        degree_type = ""

        try:
            con = sqlite3.connect("prototype/static/databases/scholarship_database.db")
        except:
            print("Can't connect to database")

        cur = con.cursor()

        #Build query
        query = "SELECT * FROM scholarship WHERE "
        parameters = []

        if not aos == "":
            print("AOS not null")
            query += "area_of_study = ? AND "
            parameters.append(aos)
        if not institution == "":
            print("Institution is not null")
            query += "institution = ? AND "
            parameters.append(institution)
        if not gender == "":
            print("gender is not null")
            query += "gender = ? AND "
            parameters.append(gender)
        if not nationality == "":
            print("nationality is not null")
            query += "nationality = ? AND "
            parameters.append(nationality)
        if not degree_type == "":
            print("degree_type is not null")
            query += "degree_type = ? AND "
            parameters.append(degree_type)

        #Make sure does not end with AND
        filter_query = query[:-5] + ";"
        print(filter_query)
        
        #execute query and get rows
        try:
            cur.execute(filter_query, parameters)
        except: 
            print("Error occured when executing query")

        #print to terminal
        rows = list(cur.fetchall())
        print(rows)

        con.close()

def filter_bursary():
    #if request.method == 'POST':
        #Get everything that should be filtered by
        #area of study, institution, gender, nationality, degree type
        #aos = request.form.get('area-of-study-filter')
        
        aos = "Any"
        institution = ""
        nationality = ""
        degree_type = ""

        with sqlite3.connect("prototype/static/databases/bursary_database.db") as con:
            cur = con.cursor()

            #Build query
            query = "SELECT * FROM bursary WHERE "
            parameters = []

            if not aos == "":
                print("AOS not null")
                query += "area_of_study = ? AND "
                parameters.append(aos)
            if not institution == "":
                print("Institution is not null")
                query += "institution = ? AND "
                parameters.append(institution)
            if not nationality == "":
                print("nationality is not null")
                query += "nationality = ? AND "
                parameters.append(nationality)
            if not degree_type == "":
                print("degree_type is not null")
                query += "degree_type = ? AND "
                parameters.append(degree_type)

            #Make sure does not end with AND
            filter_query = query[:-5] + ";"
            print(filter_query)
            
            #execute query and get rows
            cur.execute(filter_query, parameters)
            rows = list(cur.fetchall())
            
            print(rows)

        #except:
            #con = sqlite3.connect("database.db")
            #con.rollback()
            #msg = "Error occurred"
            #return render_template("result.html", msg=msg)

        #finally:
            #con.close()            



#LOADING OPTIONS
def load_scholarship_options():
    #get cursor
    if os.path.isfile("prototype/static/databases/scholarship_database.db"):
        con = sqlite3.connect("prototype/static/databases/scholarship_database.db")

    con.row_factory = sqlite3.Row
    cur = con.cursor()

    #Get distinct values for [area of study, institution, gender, nationality, degree type]
    parameters = ['area_of_study', 'institution', 'gender', 'nationality', 'degree_type']
    options = []
    for param in parameters:
        op = [] #placeholder for values
        query = "SELECT DISTINCT "+ param +" FROM scholarship;"
        cur.execute(query)
        values = cur.fetchall()
        
        for v in values:
            op.append(v[0]) #append the actual values instead of sql row object

        options.append(op)

    return options

def load_bursary_options():
    #get cursor
    if os.path.isfile("prototype/static/databases/bursary_database.db"):
        con = sqlite3.connect("prototype/static/databases/bursary_database.db")

    con.row_factory = sqlite3.Row
    cur = con.cursor()

    #Get distinct values for [area of study, institution, nationality, degree type]
    parameters = ['area_of_study', 'institution', 'nationality', 'degree_type']
    options = []
    for param in parameters:
        op = [] #placeholder for values
        query = "SELECT DISTINCT "+ param +" FROM bursary;"
        cur.execute(query)
        values = cur.fetchall()
        
        for v in values:
            op.append(v[0]) #append the actual values instead of sql row object

        options.append(op)

    return options





#Debugging
#Print all from database to terminal
@app.route("/list_bursary")
def list_bursary():
    if os.path.isfile("prototype/static/databases/bursary_database.db"):
        con = sqlite3.connect("prototype/static/databases/bursary_database.db")

    con.row_factory = sqlite3.Row
    cur = con.cursor()

    cur.execute("select * from bursary")
    
    rows = cur.fetchall()
    result = [list(i) for i in rows]
    print(result)

    return "Rows returned. Check terminal"

#Print all from database to terminal
@app.route("/list_scholarship")
def list_scholarship():
    if os.path.isfile("prototype/static/databases/scholarship_database.db"):
        con = sqlite3.connect("prototype/static/databases/scholarship_database.db")

    con.row_factory = sqlite3.Row
    cur = con.cursor()

    cur.execute("select * from scholarship")

    rows = cur.fetchall()
    result = [list(i) for i in rows]
    print(result)

    return "Rows returned. Check terminal"

#DEBUG
@app.route('/filter')
def filter():
    print("Filter scholarships")
    filter_scholarship()
    print("\n")
    print("Filter bursaries")
    filter_bursary()
    return "Check terminal"
from re import template
import sqlite3
from typing import final
from flask import Flask, request
from flask import render_template
from . import app

import os

@app.route("/")
def home():
    return "Home"

@app.route("/scholarship")
def scholarship():
    options = load_scholarship_options()
    rows = list_scholarship()
    return render_template('scholarship-search.html',aoss=options[0],institutions=options[1], genders=options[2], nationalities=options[3], degree_types=options[4], rows=rows)

@app.route("/bursary")
def bursary():
    options = load_bursary_options()
    rows = list_bursary()
    return render_template('bursary-search.html',aoss=options[0],institutions=options[1], nationalities=options[2], degree_types=options[3], rows=rows)

@app.route("/bursary-info")
def b_info():
    return render_template("bursary-info.html")

@app.route('/filter_scholarship_results', methods = ['POST', 'GET'])
def filter_scholarship_results():
    if request.method == 'POST':
        #Get everything that should be filtered by
        #area of study, institution, gender, nationality, degree type
        aos = request.form.get('area-of-study-filter') 
        institution = request.form.get('institution-filter') 
        gender = request.form.get('gender-filter')          
        nationality = request.form.get('nationality-filter') 
        degree_type = request.form.get('degree-type-filter') 

    print("Filtering conditions")
    print("AOS is "+aos)
    print("institution is "+institution)
    print("gender is "+gender)
    print("nationality is "+nationality)
    print("degree_type is "+degree_type)
    print("\n")
    
    rows = filter_scholarship(aos, institution, gender, nationality, degree_type)
    print(rows)

    return render_template('scholarship-search.html', rows=rows)

@app.route('/filter_bursary_results', methods = ['POST', 'GET'])
def filter_bursary_results():
    if request.method == 'POST':
        #Get everything that should be filtered by
        #area of study, institution, gender, nationality, degree type
        aos = request.form.get('area-of-study-filter') 
        institution = request.form.get('institution-filter')          
        nationality = request.form.get('nationality-filter') 
        degree_type = request.form.get('degree-type-filter') 

    #Debugging
    print("Filtering conditions")
    print("AOS is "+aos)
    print("institution is "+institution)
    print("nationality is "+nationality)
    print("degree_type is "+degree_type)
    print("\n")
    
    rows = filter_bursary(aos, institution, nationality, degree_type)
    print(rows)

    return render_template('bursary-search.html', rows=rows)

#ALL INFO PAGES
@app.route('/s1')
def s1():
    return render_template('scholarship_info/s1.html')

@app.route('/s2')
def s2():
    return render_template('scholarship_info/s2.html')

@app.route('/s3')
def s3():
    return render_template('scholarship_info/s3.html')

@app.route('/s4')
def s4():
    return render_template('scholarship_info/s4.html')

@app.route('/s5')
def s5():
    return render_template('scholarship_info/s5.html')

#Bursaries
@app.route('/b1')
def b1():
    return render_template('bursary_info/b1.html')

@app.route('/b2')
def b2():
    return render_template('bursary_info/b2.html')

@app.route('/b3')
def b3():
    return render_template('bursary_info/b3.html')

@app.route('/b4')
def b4():
    return render_template('bursary_info/b4.html')

@app.route('/b5')
def b5():
    return render_template('bursary_info/b5.html')

@app.route('/b6')
def b6():
    return render_template('bursary_info/b6.html')

@app.route('/b7')
def b7():
    return render_template('bursary_info/b7.html')

@app.route('/b8')
def b8():
    return render_template('bursary_info/b8.html')


#FILTER OPTIONS
def filter_scholarship(aos, institution, gender, nationality, degree_type):
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

    con.close()

    return rows

def filter_bursary(aos, institution, nationality, degree_type):
    try:
        con = sqlite3.connect("prototype/static/databases/bursary_database.db")
    except:
        print("Connection Error")

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
    try:
        cur.execute(filter_query, parameters)
    except:
        print("Cannot execute command")

    rows = list(cur.fetchall())
    
    con.close()

    return rows
                    
                       
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
    
    rows = list(cur.fetchall())

    return rows

#Print all from database to terminal
def list_scholarship():
    if os.path.isfile("prototype/static/databases/scholarship_database.db"):
        con = sqlite3.connect("prototype/static/databases/scholarship_database.db")

    con.row_factory = sqlite3.Row
    cur = con.cursor()

    cur.execute("select * from scholarship")

    rows = list(cur.fetchall())
    
    return rows

#DEBUG
@app.route('/filter')
def filter():
    print("Filter scholarships")
    filter_scholarship()
    print("\n")
    print("Filter bursaries")
    filter_bursary()
    return "Check terminal"
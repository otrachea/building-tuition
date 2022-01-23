from re import template
import sqlite3
from typing import final
from flask import Flask, request
from flask import render_template
from . import app

import os, sys

@app.route("/")
def home():
    return render_template('home.html')

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

@app.route('/filter_scholarship_results', methods = ['POST', 'GET'])
def filter_scholarship_results():
    options = load_scholarship_options()
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

    return render_template('scholarship-search.html',aoss=options[0],institutions=options[1], genders=options[2], nationalities=options[3], degree_types=options[4], rows=rows)

@app.route('/filter_bursary_results', methods = ['POST', 'GET'])
def filter_bursary_results():
    options = load_bursary_options()

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

    return render_template('bursary-search.html',aoss=options[0],institutions=options[1], nationalities=options[2], degree_types=options[3], rows=rows)

#INFO PAGES
@app.route('/<id>')
def scholarshipInfoPage(id):
    desc = """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Porta non pulvinar neque laoreet suspendisse interdum. Diam phasellus vestibulum lorem sed risus ultricies tristique. Suscipit tellus mauris a diam maecenas sed enim ut sem. Interdum velit laoreet id donec ultrices. Facilisis leo vel fringilla est ullamcorper eget nulla facilisi etiam. In nisl nisi scelerisque eu ultrices. Pharetra magna ac placerat vestibulum lectus. Sociis natoque penatibus et magnis dis parturient montes nascetur. Congue quisque egestas diam in arcu.
            Elementum curabitur vitae nunc sed velit dignissim sodales ut. Ornare massa eget egestas purus viverra accumsan in nisl nisi. Mauris commodo quis imperdiet massa tincidunt nunc pulvinar sapien et. Ac odio tempor orci dapibus ultrices in iaculis nunc sed. A pellentesque sit amet porttitor eget dolor morbi non arcu. Sed vulputate mi sit amet mauris commodo quis imperdiet massa. Sed ullamcorper morbi tincidunt ornare massa eget egestas purus viverra. Et magnis dis parturient montes nascetur ridiculus mus. Fermentum leo vel orci porta non pulvinar neque. Eget nunc lobortis mattis aliquam faucibus purus in massa.
            Amet venenatis urna cursus eget nunc scelerisque. Ut morbi tincidunt augue interdum velit. A diam maecenas sed enim. Lorem dolor sed viverra ipsum. Cursus eget nunc scelerisque viverra mauris in aliquam sem. Odio pellentesque diam volutpat commodo sed egestas egestas. Venenatis urna cursus eget nunc scelerisque viverra. Interdum velit euismod in pellentesque massa placerat. Lectus quam id leo in vitae turpis. Amet mattis vulputate enim nulla aliquet porttitor lacus luctus. Elementum sagittis vitae et leo duis ut diam. Sit amet risus nullam eget felis eget nunc. Condimentum lacinia quis vel eros donec ac odio. Eu non diam phasellus vestibulum lorem sed risus ultricies. Arcu ac tortor dignissim convallis aenean et tortor. Id volutpat lacus laoreet non curabitur.
            Dictum varius duis at consectetur. Non curabitur gravida arcu ac. Dignissim enim sit amet venenatis urna cursus eget. Justo nec ultrices dui sapien eget mi. Ipsum a arcu cursus vitae congue mauris rhoncus aenean vel. Sed lectus vestibulum mattis ullamcorper velit sed ullamcorper morbi. Scelerisque mauris pellentesque pulvinar pellentesque. Libero justo laoreet sit amet cursus sit amet dictum. Venenatis lectus magna fringilla urna porttitor rhoncus dolor purus. Est sit amet facilisis magna etiam tempor orci eu lobortis. Sodales ut eu sem integer vitae. At lectus urna duis convallis convallis tellus id. Ut enim blandit volutpat maecenas volutpat blandit aliquam etiam. Nam libero justo laoreet sit amet. Vestibulum lorem sed risus ultricies tristique nulla aliquet enim. Mauris a diam maecenas sed enim ut sem viverra. Metus vulputate eu scelerisque felis. Vestibulum rhoncus est pellentesque elit. Risus at ultrices mi tempus imperdiet nulla malesuada pellentesque. Arcu odio ut sem nulla pharetra.
            """

    if id[0] == 's': # IF SCHOLARSHIP
        row = filter_scholarship_by_id(id)[0]
        return render_template('scholarship-info.html', name=row[0], institution=row[1], amount=row[2], fos=row[3], deadline=row[4], description=desc, url=row[5])
    else: # IF BURSARY
        row = filter_bursary_by_id(id)[0]
        return render_template('bursary-info.html', name=row[0], institution=row[1], fos=row[2], description=desc, url=row[3])


#FILTER OPTIONS
def filter_scholarship(aos, institution, gender, nationality, degree_type):
    try:
        # con = sqlite3.connect("prototype/static/databases/scholarship_database.db")
        con = sqlite3.connect(os.path.dirname(os.path.abspath(__file__)).replace('\\', '/') +"/static/databases/scholarship_database.db")
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
        # con = sqlite3.connect("prototype/static/databases/bursary_database.db")
        con = sqlite3.connect(os.path.dirname(os.path.abspath(__file__)).replace('\\', '/') +"/static/databases/bursary_database.db")
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

def filter_scholarship_by_id(id):
    try:
        # con = sqlite3.connect("prototype/static/databases/scholarship_database.db")
        con = sqlite3.connect(os.path.dirname(os.path.abspath(__file__)).replace('\\', '/') +"/static/databases/scholarship_database.db")
    except:
        print("Can't connect to database")

    cur = con.cursor()

    # BUILD QUERY
    query = "SELECT name, institution, price, area_of_study, deadline, url FROM scholarship WHERE id='" + id + "'"
    try:
        cur.execute(query)
    except: 
        print("Error occured when executing query")

    row = cur.fetchall()
    con.close()

    return row

def filter_bursary_by_id(id):
    try:
    # con = sqlite3.connect("prototype/static/databases/bursary_database.db")
        con = sqlite3.connect(os.path.dirname(os.path.abspath(__file__)).replace('\\', '/') +"/static/databases/bursary_database.db")
    except:
        print("Can't connect to database")

    cur = con.cursor()

    # BUILD QUERY
    query = "SELECT name, institution, area_of_study, url FROM bursary WHERE id='" + id + "'"
    try:
        cur.execute(query)
    except: 
        print("Error occured when executing query")

    row = cur.fetchall()
    con.close()

    return row                    


#LOADING OPTIONS
def load_scholarship_options():
    #get cursor
    # if os.path.isfile("prototype/static/databases/scholarship_database.db"):
        # con = sqlite3.connect("prototype/static/databases/scholarship_database.db")

    path = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/') +"/static/databases/scholarship_database.db"
    if os.path.isfile(path):
        con = sqlite3.connect(path)

    con.row_factory = sqlite3.Row
    cur = con.cursor()

    #Get distinct values for [area of study, institution, gender, nationality, degree type]
    parameters = ['area_of_study', 'institution', 'gender', 'nationality', 'degree_type']
    options = []
    for param in parameters:
        op = [] #placeholder for values
        query = "SELECT DISTINCT "+ param +" FROM scholarship ORDER BY "+ param +" ASC;"
        cur.execute(query)
        values = cur.fetchall()
        
        for v in values:
            op.append(v[0]) #append the actual values instead of sql row object

        options.append(op)

    return options

def load_bursary_options():
    #get cursor
    # if os.path.isfile("prototype/static/databases/bursary_database.db"):
    #     con = sqlite3.connect("prototype/static/databases/bursary_database.db")

    path = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/') +"/static/databases/bursary_database.db"
    if os.path.isfile(path):
        con = sqlite3.connect(path)

    con.row_factory = sqlite3.Row
    cur = con.cursor()

    #Get distinct values for [area of study, institution, nationality, degree type]
    parameters = ['area_of_study', 'institution', 'nationality', 'degree_type']
    options = []
    for param in parameters:
        op = [] #placeholder for values
        query = "SELECT DISTINCT "+ param +" FROM bursary ORDER BY "+ param +" ASC;"
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
    # if os.path.isfile("prototype/static/databases/bursary_database.db"):
    #     con = sqlite3.connect("prototype/static/databases/bursary_database.db")

    path = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/') +"/static/databases/bursary_database.db"
    if os.path.isfile(path):
        con = sqlite3.connect(path)

    con.row_factory = sqlite3.Row
    cur = con.cursor()

    cur.execute("select * from bursary")
    
    rows = list(cur.fetchall())

    return rows

#Print all from database to terminal
def list_scholarship():
    # if os.path.isfile("prototype/static/databases/scholarship_database.db"):
    #     con = sqlite3.connect("prototype/static/databases/scholarship_database.db")

    path = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/') +"/static/databases/scholarship_database.db"
    if os.path.isfile(path):
        con = sqlite3.connect(path)

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
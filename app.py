#! /usr/bin/python3

"""
This is an example Flask | Python | Psycopg2 | PostgreSQL
application that connects to the 7dbs database from Chapter 2 of
_Seven Databases in Seven Weeks Second Edition_
by Luc Perkins with Eric Redmond and Jim R. Wilson.
The CSC 315 Virtual Machine is assumed.

John DeGood
degoodj@tcnj.edu
The College of New Jersey
Spring 2020

----

One-Time Installation

You must perform this one-time installation in the CSC 315 VM:

# install python pip and psycopg2 packages
sudo pacman -Syu
sudo pacman -S python-pip python-psycopg2 python-flask

----

Usage

To run the Flask application, simply execute:

export FLASK_APP=app.py 
flask run
# then browse to http://127.0.0.1:5000/

----

References

Flask documentation:  
https://flask.palletsprojects.com/  

Psycopg documentation:
https://www.psycopg.org/

This example code is derived from:
https://www.postgresqltutorial.com/postgresql-python/
https://scoutapm.com/blog/python-flask-tutorial-getting-started-with-flask
https://www.geeksforgeeks.org/python-using-for-loop-in-flask/
"""

import psycopg2
from config import config
from flask import Flask, render_template, request

# Connect to the PostgreSQL database server
def connect(query_handler):
    conn = None
    #rows = []
    try:
        # read connection parameters
        params = config()
 
        # connect to the PostgreSQL server
        print('Connecting to the %s database...' % (params['database']))
        conn = psycopg2.connect(**params)
        print('Connected.')
      
        # create a cursor
        cur = conn.cursor()
        
        # execute a query using fetchall()
        cur.execute(query_handler)
        rows = cur.fetchall()

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print("HELP")
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
    # return the query result from fetchall()
    return rows
 
# app.py
app = Flask(__name__)


# serve form web page
@app.route("/")
def form():
    return render_template('goat-form.html')

# handle venue POST and serve result web page
# @app.route('/kids-handler', methods=['POST'])
# def venue_handler():
#     currnet_goat_id = request.form['goat_id']
#     print(currnet_goat_id)
#     kids = connect('SELECT kid_id FROM parentof WHERE parent_id = \'' + currnet_goat_id + '\';')
#     #heads = ['kid_id']
#     return render_template('my-result.html', kids=kids, current=currnet_goat_id)
# @app.route('/EID-search', methods=['POST'])
# def EID_search():
#     print('---------------- EID == ' + request.form['EID'])
#     rows = connect('SELECT goat_id, status FROM goat WHERE goat_id = ' + request.form['eid'] + ';')
#     heads = ['goat_id', 'status']
#     return render_template('progeny-report-result.html', rows=rows, heads=heads)

# handle venue POST and serve result web page
@app.route('/progeny-handler/<string:prog_tag>', methods=['GET','POST'])
def venue_handler(prog_tag):
    # check if given tag contains single quotes ('') around itself
    # if not found on either side, add them for use in queries
    requested_goat = prog_tag
    if requested_goat[0] != '\'':
        requested_goat = '\'' + requested_goat
    if requested_goat[-1] != '\'':
        requested_goat = requested_goat + '\''


    # FInd basic info
    query =  'SELECT *' + ' '
    query += 'FROM goat' + ' '
    query += 'WHERE goat_id =' + requested_goat + ';'
    print('goat_info = ' + query)
    rows = connect(query)

    # Find IDs
    query =  'SELECT *' + ' '
    query += 'FROM GOATIDS' + ' '
    query += 'WHERE goat_id = ' + requested_goat + ';'
    print('goat_ids = ' + query)
    goat_ids = connect(query)

    # Find weights
    query =  'SELECT trait_text, alpha_value, when_measured' + ' '
    query += 'FROM (' + ' '
    query +=   'SELECT *' + ' '
    query +=   'FROM weighed AS W1,weight AS W2' + ' '
    query +=   'WHERE goatid = ' + requested_goat + ' '
    query +=     'and W1.weightid=W2.weightid' + ' '
    query +=     'and W2.alpha_value !=\'\'' + ' '
    query +=   'ORDER BY when_measured' + ' '
    query += ')' + ' '
    query += 'ORDER BY trait_code' + ';'
    print('goat_weights = ' + query)
    goat_weights = connect(query)
    
    # Find counts of kids by sex
    query =  'SELECT DISTINCT sex,COUNT(sex)' + ' '
    query += 'FROM parentof,goat' + ' '
    query += 'WHERE parent_id = ' + requested_goat + ' '
    query +=   'and kid_id=goat_id' + ' '
    query += 'GROUP BY sex' + ';'
    print('goat_kids_counts = ' + query)
    goat_kids_counts = connect(query)
    
    # Find kids
    query =  'SELECT kid_id,sex,status,dob' + ' '
    query += 'FROM parentof,goat' + ' '
    query += 'WHERE parent_id = ' + requested_goat + ' '
    query +=   'and kid_id=goat_id' + ';'
    print('goat_kids = ' + query)
    goat_kids = connect(query)
    
    # Find notes
    query =  'SELECT G.notetext,G.createddate' + ' '
    query += 'FROM hasnote AS H,gnote AS G' + ' '
    query += 'WHERE G.noteid = H.noteid' + ' '
    query +=   'and H.goatid = ' + requested_goat + ';'
    print('goat_notes = ' + query)
    goat_notes = connect(query)

    # Single line version of queries
    # Used to be used, but multi line was clearer
    # keep just to reference if one of the above breaks

    #rows = connect('SELECT * FROM goat WHERE goat_id = ' + request.form['goat_id'] + ';')
    #goat_ids = connect('SELECT * from GOATIDS WHERE goat_id = ' + request.form['goat_id']  + ';')
    #goat_weights = connect('select * from (select trait_text, alpha_value, when_measured from weighed AS W1,weight AS W2 where goatid = ' + request.form['goat_id']  + ' and W1.weightid=W2.weightid and W2.alpha_value !=\'\' order by when_measured ASC, trait_code ASC;')
    #goat_kids_counts = connect('SELECT DISTINCT sex,COUNT(sex) from parentof,goat where parent_id = ' + request.form['goat_id'] + ' and kid_id=goat_id GROUP BY sex;')
    #goat_kids = connect('select kid_id,sex,status,dob from parentof,goat where parent_id = ' + request.form['goat_id'] + ' and kid_id=goat_id;')
    #goat_notes = connect('select G.notetext,G.createddate from hasnote AS H,gnote AS G where G.noteid = H.noteid and H.goatid = ' + request.form['goat_id'] + ';')

    return render_template('progeny-report-result.html', current_goat=requested_goat, goat_info=rows, goat_ids=goat_ids, goat_weights=goat_weights, goat_kids_counts=goat_kids_counts, goat_kids=goat_kids, goat_notes=goat_notes)

# handle query POST and serve result web page
@app.route('/familytree-handler/<string:goat_tag>', methods=['GET','POST'])
def query_handler(goat_tag):
    # check if given tag contains single quotes ('') around itself
    # if not found on either side, add them for use in queries
    requested_goat = goat_tag
    if requested_goat[0] != '\'':
        requested_goat = '\'' + requested_goat
    if requested_goat[-1] != '\'':
        requested_goat = requested_goat + '\''

    # Find parents
    query =  'SELECT parent_id, dam_or_sire' + ' '
    query += 'FROM parentof' + ' '
    query += 'WHERE kid_id = ' + requested_goat + ';'
    parents = connect(query)
    # Capitilize parent type if lowercase
    parents_corrected = []
    for parent in parents:
        if parent[1] == 'dam':
            parent_type = 'Dam'
        else:
            parent_type = 'Sire'
        parents_corrected.append([parent[0], parent_type])

    # Find kids
    query =  'SELECT kid_id,sex' + ' '
    query += 'FROM parentof,goat' + ' '
    query += 'WHERE parent_id = ' + requested_goat + ' '
    query +=   ' AND kid_id = goat_id' + ';'
    kids = connect(query)

    # Find sex of current goat
    query =  'SELECT goat_id, sex' + ' '
    query += 'FROM goat' + ' '
    query += 'WHERE goat_id = ' + requested_goat + ';'
    requested_goat_data = connect(query)
    if requested_goat_data:
        # If the data was found, get the correct row
        # connect will return result as a 2D array [[data], [data], etc]
        # Since our result (should) only return a single row, we just need to get that out of the 2D array
        requested_goat_correct = requested_goat_data[0]
    else:
        # if the data wasn't found the current goat is likely a member of the found pack and doesn't have an entry in the goat table
        # instead we can query for the type of parent they are, based of that we can assume their sex
        # Note: this will not properly represent goat that aren't male nor female, but we can't know what they are either way due to lack of data
        query =  'SELECT DISTINCT parent_id, dam_or_sire' + ' '
        query += 'FROM parentof' + ' '
        query += 'WHERE parent_id = ' + requested_goat + ';'
        requested_goat_data = connect(query)[0]
        # Based on the parent type of this goat find the assumed sex
        if requested_goat_data[1] == 'dam':
            requested_goat_gender = 'Female'
        else:
            requested_goat_gender = 'Male'
        
        requested_goat_correct = [requested_goat_data[0],requested_goat_gender]

    #parents = connect('select parent_id,dam_or_sire from parentof where kid_id = '+ current +';')
    #kids = connect('select kid_id,dam_or_sire from parentof where parent_id = '+ current +';')

    return render_template('test-free.html', current_goat=requested_goat_correct, parents=parents_corrected, kids=kids)

if __name__ == '__main__':
    app.run(debug = True)

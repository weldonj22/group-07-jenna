# Project Overview
The goal of this project was to create two modules, the progeny report and goat family tree. The progeny report displays information about a goat as well as its kids. The family tree displays any known parents and kids of a given goat.

# Goat DB
## Creating the Database

To create the database, run the python script createdb.py


```
$ python createdb.py
```

This script will handle the following steps:

1. Dropping and Generating a new database
2. Generating new tables using tables.sql
3. Generating insert.sql, containing thousands of INSERT commands for populating the database with data taken from:
    - Animal.csv
    - Note.csv
    - PicklistValue.csv
    - SessionAnimalActivity.csv
    - SessionAnimalTrait.csv
4. Executing insert.sql
5. Generating views based on the tables
6. Running test queries, allowing the user to verify successful execution of the test queries

All steps listed above are accompanied by printed statements to inform the user of which step is taking place at any one time.

Note: Due to the amount of INSERTs in insert.sql, it may take noticably longer than the other steps. Please be patient.

## Using the Database with psql

To use the database with psql, use the command:

```
psql goat
```

Once inside psql, the following tables can be queried:
- Goat
    - goat_id (tag of goat)
    - sex
    - status
    - dob (date of birth)
- Goat_ids
    - goat_id (tag of goat)
    - rfid
    - nlis
- Weight
    - weightid
    - alphavalue
    - when_measured
    - trait_code
    - trait_text
- Gnote (Goat Note)
    - noteid
    - note_text
    - createddate (date created)
- Parent_of
    - parent_id (tag of parent)
    - kid_id (tag of kid)
    - dam_or_sire
- Weighed
    - goatid (tag of goat)
    - weightid
- HasNote
    - goatid (tag of goat)
    - noteid

# The Web App
## Prerequisites
Make sure the following python packages are installed:
- pip
- psycopgs2 (also needed to run database creation script)
- flask

## Running the server
Run the following the commands:

```
export FLASK_APP=app.py
```
```
flask run
```

## Using the website
With the server running, navigate to the following IP in a web browser, or click the link for it displayed in the terminal the server is running in.
```
127.0.0.1
```
### Home Page
![Home Page](/images/home_page.png)
The Home Page allows the user to navigate to either the progeny report or family tree. If the user wishes to go to either of the two for a particular goat, they must enter the tag of that goat in the box below the corresponding prompt, then press the "Search" button below it.

### Progeny Report
![Information and weights from progeny report for 15091](/images/progeny_report.png)
At the top of the page there a button to either take the user back to the home page, or to the family tree of the goat whose progeny report is being displayed.

The following information is listed on this page:
1. Basic information<br>
    Various details about the goat including its current status, sex, date of birth, RFID, and NLIS.

2. Weight<br>
    A list of weight records. The type of each weight is displayed in text on the left side, while the center column is the value of the weight (in pounds), and the rightmost is the date the weight was recorded.

![View of kids and notes in progeny report for goat 10001](/images/progeny_report_2.png)
3. Kids<br>
    Starts with a list of counts for the sexes of all the goat's kids. Note that the page will only display sexes for which the goat has at least one kid of. For example, if a goat only has 4 females, then only "Female: 4" will be listed.
    <br><br>
    Additionally, a table is displayed consisting of each kid of the goat, showing its tag, sex, status, and date of birth.

4. Notes<br>
    A list of notes recorded for each goat. Displayed as a table, it consists of the text of the note in the first column, and the date of creation in the second.

### Family Tree
![Family Tree](/images/family_tree.png)
The family tree displays the parents and kids of the "current" goat. For either parents or kids, only the correct amount of each will be displayed. For each displayed goat, including the current, there are a 4 boxes that make up the node. For top left, going clockwise: <br>
1. the goat's tag
2. a button linking to the goat's progeny report
3. a button linking to the family tree of the goat (where it is the current)
4. the sex of the goat, for parents it is denoted by its gendered parent type (dam for females, sire for males)
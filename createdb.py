import psycopg2
import csv
import os

command_count = 1 # count of executed INSERTs
unadded_parentof = {} # parent-kid combos for goat whose kid is inserted before they are
goat_id_tag = {} # Lookup for tags based on ID

# Attempt to execute an INSERT
def try_insert(command):
   global command_count
   try:
      cursor.execute(command) # execute the command
   # INSERTed value does not match defined restrictions
   except psycopg2.errors.StringDataRightTruncation:
      # print error, including lengths of each value given
      print(str(command_count) + ': SDRT for \n\t' + command)
      for col in command[command.index('(')+1:-2].split(','):
         print(col + ': ' + str(len(col)))
   # the values of the primary key are not unique
   except psycopg2.errors.UniqueViolation:
      print(str(command_count) + ': UV for \n\t' + command)
   command_count += 1

# Handle dropping/creating the DB
conn = psycopg2.connect(
   database="postgres", user='postgres', password='password', host='127.0.0.1', port= '5432'
)
conn.autocommit = True
cursor = conn.cursor()

# Drop existing Database
print('Dropping DB\n')
cursor.execute("DROP DATABASE IF EXISTS goat")

# create the database
print('Creating new DB\n')
cursor.execute("CREATE database goat")

conn.close()

# Connect to newly created goat DB
conn = psycopg2.connect(
   dbname="goat", user='postgres', password='password', host='127.0.0.1', port= '5432'
)
conn.autocommit = True
cursor = conn.cursor()

# run schema.sql to establish the tables
print('Creating tables\n')
with open("data/our_tables.sql", 'r') as file:
   schema = file.read()
   cursor.execute(schema)

goat_ids = {}

# Generate INSERTs for tables

print('Generating INSERTs for tables Goat,GoatIDs,ParentOf\n')
with open('data/Animal.csv', 'r') as animalCSV:
   reader = csv.reader(animalCSV)
   next(reader) # skip header line
   
   for row in reader:
      # Get tag of goat
      goat_tag = row[2]

      # Enter tag into tag lookup for later use
      goat_id_tag[row[0]] = goat_tag

      # Get basic information
      goat_sex = row[7]
      goat_status = row[25]
      goat_dob = row[8]
      if goat_dob == '':
         goat_dob = 'NULL'

      # Generate query to insert into GOAT
      command = 'INSERT INTO GOAT VALUES ('
      command += '\'' + goat_tag + '\','
      command += '\'' + goat_sex + '\','
      command += '\'' + goat_status + '\','
      if goat_dob == 'NULL': # Add single qoutes around dob if not null
         command += 'NULL'
      else:
         command += '\'' + goat_dob + '\''
      command += ');'
      try_insert(command)

      # Get tag of the dam
      goat_dam_tag = row[10]
      goat_dam_id = ''
      
      # If not unknown
      if goat_dam_tag.strip().lower() not in ['', 'unknown', 'notag']:

         # the tags of some dams, as listed by their kids, are not actual tags, but their RFIDs
         # in these cases, the correct tag is provided
         if goat_dam_tag == '964 001009986693':
            goat_dam_tag = 'OR0415'
         elif goat_dam_tag == '964001027785070':
            goat_dam_tag = 'OR02463'

         # generate and execute the INSERT
         command = 'INSERT INTO PARENTOF VALUES ('
         command += '\'' + goat_dam_tag + '\','
         command += '\'' + goat_tag + '\','
         command += '\'dam\''
         command += ');'
         try_insert(command)
      
      # Get tag of sire
      goat_sire_tag = row[9]
      
      # if a valid tag was given, generate the INSERT and execute it
      if goat_sire_tag.strip().lower() not in ['', 'unknown', 'notag']:
         command = 'INSERT INTO PARENTOF VALUES ('
         command += '\'' + goat_sire_tag + '\','
         command += '\'' + goat_tag + '\','
         command += '\'sire\''
         command += ');'
         try_insert(command)

      # Get IDs
      goat_rfid = row[3]
      goat_nlis = row[4]

      # insert into GOATIDS
      command = 'INSERT INTO GOATIDS VALUES ('
      command += '\'' + goat_tag + '\','
      command += '\'' + goat_rfid + '\','
      command += '\'' + goat_nlis + '\''
      command += ');'
      try_insert(command)


   print('Generating INSERTs for tables: GNote,HasNote\n') 
   with open('data/Note.csv', 'r') as noteCSV:
      reader = csv.reader(noteCSV)
      next(reader) # skip header line
   
      for row in reader:

         # Get note details
         gnote_text = row[2]
         gnote_date = row[1]

         # insert into gnote
         command = 'INSERT INTO GNOTE (notetext,createddate) VALUES ('
         command += '\'' + gnote_text + '\','
         command += '\'' + gnote_date + '\''
         command += ') RETURNING noteID;' # return the ID of the newly inserted note
         try_insert(command)

         # Get data goat tag and note_id
         hasNote_goat_tag = goat_id_tag[row[0]]
         hasNote_note_id = str(cursor.fetchone()[0])

         # insert into HasNote
         command = 'INSERT INTO HASNOTE VALUES ('
         command += '\'' + hasNote_goat_tag + '\','
         command += '\'' + hasNote_note_id + '\''
         command += ');'
         try_insert(command)

   # dictionary for looking up trait text from codes
   trait_text = {
      '53': 'Live Weight',
      '357': 'Birth Weight',
      '405': 'YWT', # Yearly Weight?
      '952': 'Project Weight',
      '963': 'Live Weight',
      '970': 'Turn out weight'
   }

   print('Generating INSERTs for tables: Weight,Weighed\n') 
   with open('data/SessionAnimalTrait.csv', 'r') as noteCSV:
      reader = csv.reader(noteCSV)
      next(reader) # skip header line
   

      for row in reader:
         # Get code
         weight_trait_code = row[2]
         # if code is not a weight code, ignore
         if weight_trait_code not in ['53','357','405','952','963','970']:
            continue
         
         # get details of weight record
         weight_value = row[3]
         weight_date = row[5]
         weight_trait_code_text = trait_text[weight_trait_code]

         # insert weight into Weight table
         command = 'INSERT INTO WEIGHT (alpha_value, when_measured, trait_code, trait_text) VALUES ('
         command += '\'' + weight_value + '\','
         command += '\'' + weight_date + '\','
         command += '\'' + weight_trait_code + '\','
         command += '\'' + weight_trait_code_text + '\''
         command += ') RETURNING weightID;' # get ID of newly inserted weight
         try_insert(command)

         # fetch the weight_id
         weight_id = str(cursor.fetchone()[0])
         # try to get the tag of the fetched ID
         try:
            weight_goat_id = goat_id_tag[row[1]]
         # print an error if there is an invalid goat_id
         # at this point all valid goats have been added, if the ID can't be found, something else is wrong
         except KeyError:
            print('tag for id = ' + row[0] + ' could not be found')

         # insert into weighed
         command = 'INSERT INTO WEIGHED VALUES ('
         command += '\'' + weight_goat_id + '\','
         command += '\'' + weight_id + '\''
         command += ');'
         try_insert(command)

#Close the connection
conn.close()
print('GoatDB Created Successfully\n')
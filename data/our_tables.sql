
DROP TABLE IF EXISTS Goat;
CREATE TABLE Goat (
    goat_id varchar(20) NOT NULL primary key,
    sex varchar(20) NOT NULL default '',
    status varchar(20) NOT NULL default '',
    dob timestamp
);

DROP TABLE IF EXISTS GoatIDs;
CREATE TABLE GoatIDs (
	goat_id varchar(20) primary key,
    rfid varchar(15) NOT NULL default '',
	nlis varchar(16) NOT NULL default ''
);

DROP TABLE IF EXISTS Weight;
CREATE TABLE Weight (
    weightID integer GENERATED ALWAYS AS IDENTITY primary key,
    alpha_value varchar(20) NOT NULL default '',
    when_measured timestamp NOT NULL,
    trait_code integer NOT NULL,
    trait_text varchar(15)
);

DROP TABLE IF EXISTS GNote;
CREATE TABLE GNote (
    noteID integer GENERATED ALWAYS AS IDENTITY primary key,
    notetext varchar(30) NOT NULL,
    createddate timestamp
);

DROP TABLE IF EXISTS ParentOf;
CREATE TABLE ParentOf (
    parent_id varchar(20) NOT NULL,
    kid_id varchar(20) NOT NULL,
    dam_or_sire varchar(4) NOT NULL,
	primary key( parent_id,kid_id )
);

DROP TABLE IF EXISTS Weighed;
CREATE TABLE Weighed (
    goatid varchar(20) NOT NULL,
    weightid integer NOT NULL,
	primary key( goatid,weightid )
);

DROP TABLE IF EXISTS HasNote;
CREATE TABLE HasNote (
    goatid varchar(20) NOT NULL,
    noteid integer,
	primary key( goatid,noteid )
);
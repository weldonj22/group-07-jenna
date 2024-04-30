-- Testing goat
-- a. Display info for the goat with an EID of 964001009986941
(
    SELECT *
    FROM goat
    WHERE eid = '964001009986841'
) LIMIT 10;


-- b. List all female goats born on 1/28/2012
(
    SELECT *
    FROM goat
    WHERE gender = 'Female' and dob = '1/28/2012'
) LIMIT 10;


-- c. List all current goats born after During March 2016
(
    SELECT *
    FROM goat
    WHERE status = 'Current' and dob > '2/28/2016' and dob < '4/1/2016'
) LIMIT 10;


-- Testing goat_ids
-- a. Find the visualtag of the goat with an EID of 964001009986941
(
    SELECT visualtag
    FROM goat_ids
    WHERE eid = '964001009986941'
) LIMIT 10;


-- Testing weight
-- a. Determine the average live weight of goats measured on 9/14/2004
(
    SELECT AVG(CAST(weightvalue AS real)) 
    FROM weight
    WHERE weightvalue <> ''
        and date >= '9/14/2004'
        and type = '53'
)   LIMIT 10;

-- Testing note
-- a. Find all the notes created in December 2018
(
    SELECT *
    FROM gnote
    WHERE createddate >= '12/1/2018'
        and createddate < '1/1/2019'
)   LIMIT 10;

-- Testing parent_of
-- a. Get all kids of the goat with parent_id WAST03

(
    SELECT *
    FROM parent_of
    WHERE parent_id = 'WAST03'
) LIMIT 10;

-- Testing weighed
-- a. Get all weights for the goat with EID = 3097
(
    SELECT weightid
    FROM weighed
    WHERE goatid = '3097'
) LIMIT 10;

-- Testing has
-- a. Get all notes for the goat with EID = 3120
(
    SELECT *
    FROM has
    WHERE goatid = '3120'
) LIMIT 10;


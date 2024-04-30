DROP VIEW IF EXISTS goat;
CREATE VIEW goat (eid, gender, status, dob) as
SELECT rfid, sex, status, dob
FROM animal;

DROP VIEW IF EXISTS goat_ids;
CREATE VIEW goat_ids (eid, visualtag) AS
SELECT rfid, tag
FROM animal;

DROP VIEW IF EXISTS weight;
CREATE VIEW weight (weightvalue, date, type) AS
SELECT alpha_value, when_measured, trait_code
FROM SessionAnimalTrait
WHERE trait_code in ('53', '357', '405', '952', '963', '970');

DROP VIEW IF EXISTS gnote;
CREATE VIEW gnote (notetext, createddate) AS
SELECT note, created
FROM note;

DROP VIEW IF EXISTS parent_of;
CREATE VIEW parent_of (parent_id, kid_id, dam_or_sire) AS
(
    SELECT dam, rfid, 'dam'
    FROM animal
    WHERE dam IS NOT NULL
)
UNION ALL
(
    SELECT sire, rfid, 'sire'
    FROM animal
    WHERE sire IS NOT NULL
);

DROP VIEW IF EXISTS weighed;
CREATE VIEW weighed (goatid, weightid) AS
SELECT animal_id, session_id
FROM SessionAnimalActivity;

DROP VIEW IF EXISTS has;
CREATE VIEW has (goatid, noteid) AS
SELECT animal_id, created
FROM note;
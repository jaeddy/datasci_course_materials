-- Problem 3h
SELECT
--     d.docid AS doc1, 
--     dt.docid AS doc2, 
    SUM(d.count * dt.count) AS similarity
    FROM frequency d, frequency dt
    WHERE
    d.term = dt.term AND
    d.docid = "10080_txt_crude" AND
    dt.docid = "17035_txt_earn"
    GROUP BY
    d.docid, dt.docid;
    
-- Problem 3i
DROP VIEW IF EXISTS SearchDocs;

CREATE VIEW [SearchDocs] AS
SELECT * FROM frequency
UNION
SELECT "q" AS docid, "washington" AS term, 1 AS count 
UNION
SELECT "q" AS docid, "taxes" AS term, 1 AS count
UNION 
SELECT "q" AS docid, "treasury" AS term, 1 AS count;

SELECT MAX(similarity) FROM (
    SELECT
        d.docid AS doc1, 
        dt.docid AS doc2, 
        SUM(d.count * dt.count) AS similarity
        FROM SearchDocs AS d, SearchDocs AS dt
        WHERE
        d.term = dt.term AND
        d.docid = "q" AND NOT dt.docid = "q"
        GROUP BY
        d.docid, dt.docid
        ORDER BY similarity DESC
);


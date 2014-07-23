-- Problem 1a
SELECT COUNT(*) FROM frequency WHERE docid = "10398_txt_earn";

-- Problem 1b
SELECT COUNT(*) FROM (
    SELECT term FROM frequency
        WHERE
        docid = "10398_txt_earn" AND
        count = 1
);
    
-- Problem 1c
SELECT COUNT(*) FROM (
    SELECT term FROM frequency
        WHERE
        docid = "10398_txt_earn" AND
        count = 1
    UNION
    SELECT term FROM frequency
        WHERE 
        docid = "925_txt_trade" AND
        count = 1
);

-- Problem 1d
SELECT COUNT(*) FROM (
    SELECT * FROM frequency
        WHERE
        term LIKE "parliament"
);

-- Problem 1e
SELECT COUNT(*) FROM (
    SELECT docid, SUM(count) AS NumberOfTerms FROM frequency
    GROUP BY docid
    HAVING SUM(count) > 300
);

-- Problem 1f
SELECT COUNT(*) FROM (
    SELECT docid FROM frequency
        WHERE
        term LIKE "transactions"
    INTERSECT
    SELECT docid FROM frequency
        WHERE 
        term LIKE "world"
);
        
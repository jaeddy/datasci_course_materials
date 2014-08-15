register s3n://uw-cse-344-oregon.aws.amazon.com/myudfs.jar

-- load the test file into Pig
raw = LOAD 's3n://uw-cse-344-oregon.aws.amazon.com/cse344-test-file' USING TextLoader as (line:chararray);

-- loading files for assignment:
-- raw = LOAD 's3n://uw-cse-344-oregon.aws.amazon.com/btc-2010-chunk-000' USING TextLoader as (line:chararray); 


-- parse each line into ntriples
ntriples = foreach raw generate FLATTEN(myudfs.RDFSplit3(line)) as (subject:chararray,predicate:chararray,object:chararray);

-- filter data to only include tuples whose subject matches rdfabout.com
biz = filter ntriples by subject matches '.*business.*';

-- create a copy of the data
biz2 = foreach biz generate subject as subject2, predicate as predicate2, object as object2;

-- perform join
biz_join = join biz by subject left outer, biz2 by subject2 PARALLEL 50;

-- remove duplicates
biz_distinct = distinct biz_join;

-- store the results in the folder /user/hadoop/prob3a
store biz_distinct into '/user/hadoop/prob3a' using PigStorage();


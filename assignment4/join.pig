register s3n://uw-cse-344-oregon.aws.amazon.com/myudfs.jar

-- load the test file into Pig
-- raw = LOAD 's3n://uw-cse-344-oregon.aws.amazon.com/cse344-test-file' USING TextLoader as (line:chararray);

-- loading files for assignment:
raw = LOAD 's3n://uw-cse-344-oregon.aws.amazon.com/btc-2010-chunk-000' USING TextLoader as (line:chararray); 


-- parse each line into ntriples
ntriples = foreach raw generate FLATTEN(myudfs.RDFSplit3(line)) as (subject:chararray,predicate:chararray,object:chararray);

-- filter data to only include tuples whose subject matches rdfabout.com
rdfabout = filter ntriples by subject matches '.*rdfabout\\.com.*';

-- create a copy of the data
rdfabout2 = foreach rdfabout generate subject as subject2, predicate as predicate2, object as object2;

-- perform join
rdfabout_join = join rdfabout by object, rdfabout2 by subject2 PARALLEL 50;

-- remove duplicates
rdfabout_distinct = distinct rdfabout_join;

-- store the results in the folder /user/hadoop/prob3b
store rdfabout_distinct into '/user/hadoop/prob3b_2' using PigStorage();



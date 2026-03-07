CREATE OR REPLACE TABLE hate_crimes AS
SELECT *
FROM read_csv_auto('NYPD_Hate_Crimes_20260213.csv');

CREATE TABLE users (
    username TEXT,
    age INTEGER,
    country TEXT
);
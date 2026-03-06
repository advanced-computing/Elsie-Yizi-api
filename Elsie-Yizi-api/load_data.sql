CREATE OR REPLACE TABLE hate_crimes AS
SELECT *
FROM read_csv_auto('Elsie-Yizi-api/NYPD_Hate_Crimes_20260213.csv');

CREATE TABLE users (
    username VARCHAR,
    age INTEGER,
    country VARCHAR
);
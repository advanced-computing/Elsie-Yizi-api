
# Profiling Takeaways – NYPD Hate Crimes Dataset

## Takeaway 1: Arrest Date is completely missing (100% null values)

The "Arrest Date" column contains 0 non-null values out of all 574 rows, meaning the column is entirely empty. 
This suggests either arrests have not been recorded in this dataset or the data was not properly formatted to be detect by Data Wrangler.

## Takeaway 2: Arrest Id has a large amount of missing data (~63% missing)

The "Arrest Id" column has 363 missing values out of 574 (~63%), meaning that the complaints are only recorded partially of all the arrests.

This may mean that some of the complaints may not result in arrests, or the arrest data may be incomplete.

## Takeaway 3: Record Create Date is stored as a string instead of datetime

The "Record Create Date" column is stored as a string instead of a datetime datatype.

This can cause problems for time-based analysis, sorting by date, and calculating trends over time.

## Takeaway 4: Full Complaint ID appears to uniquely identify each record

The "Full Complaint ID" column has 574 non-null values and appears to uniquely identify complaints, with no missing values.

This makes it suitable to use as a primary key to check if there are duplicated records. This column should not contain duplicats.

## Takeaway 5: Borough Name contains no missing values and consistent categories

The " Borough" column contains no missing values, indicating that borough information is consistently recorded for every complaint. This column appears reliable for grouping and analyzing hate crime incidents by geographic patrol borough.

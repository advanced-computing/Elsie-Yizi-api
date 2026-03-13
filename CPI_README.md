# Usage and Manual Testing Instructions

## Setup

Initialize the database using the file `PCPI24M1.csv`.  
This creates three tables:

- `cpi_append`
- `cpi_trunc`
- `cpi_inc`

All three tables initially contain the same CPI data.


## Testing Update Methods

Use the updated dataset `PCPI25M2.csv` to simulate a new CPI release.

### Append

- Inserts all rows from the new dataset.
- Existing rows are not updated.

Result:  
The table may contain **duplicate dates** if historical values were revised.


### Truncate

- Deletes all existing rows.
- Reloads the entire updated dataset.

Result:  
The table becomes an exact copy of the new dataset.


### Incremental

- Updates existing rows if values changed.
- Inserts rows for new months.

Result:  
The table contains the latest CPI data with **no duplicates**.
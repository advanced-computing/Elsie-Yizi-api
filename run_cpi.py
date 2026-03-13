import duckdb

con = duckdb.connect("lab8.duckdb")

print(
    con.execute("""
    SELECT COUNT(*) AS total_rows,
           COUNT(DISTINCT date) AS distinct_dates
    FROM cpi_inc
""").df()
)

con.close()

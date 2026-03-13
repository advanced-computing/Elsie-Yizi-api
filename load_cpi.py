import duckdb
import pandas as pd

DB_FILE = "lab8.duckdb"
FILE_2024 = "PCPI24M1.csv"
FILE_2025 = "PCPI25M2.csv"


def read_cpi_file(csv_file: str) -> pd.DataFrame:
    """
    Read a CPI csv file with columns DATE and CPI.
    Return a dataframe with columns: date, cpi
    """
    df = pd.read_csv(csv_file)
    df = df.rename(columns={"DATE": "date", "CPI": "cpi"})
    return df[["date", "cpi"]]


def initialize_database():
    """
    Create persistent database with three tables:
    cpi_append, cpi_trunc, cpi_inc
    using PCPI24M1.csv
    """
    con = duckdb.connect(DB_FILE)

    df_init = read_cpi_file(FILE_2024)

    con.execute("DROP TABLE IF EXISTS cpi_append")
    con.execute("DROP TABLE IF EXISTS cpi_trunc")
    con.execute("DROP TABLE IF EXISTS cpi_inc")

    con.register("df_init", df_init)

    con.execute("""
        CREATE TABLE cpi_append AS
        SELECT * FROM df_init
    """)

    con.execute("""
        CREATE TABLE cpi_trunc AS
        SELECT * FROM df_init
    """)

    con.execute("""
        CREATE TABLE cpi_inc AS
        SELECT * FROM df_init
    """)

    con.unregister("df_init")
    con.close()


def load_append():
    """
    Append the 2025 file to cpi_append.
    """
    con = duckdb.connect(DB_FILE)
    df_new = read_cpi_file(FILE_2025)

    con.register("df_new", df_new)

    con.execute("""
        INSERT INTO cpi_append
        SELECT * FROM df_new
    """)

    con.unregister("df_new")
    con.close()


def load_trunc():
    """
    Replace all rows in cpi_trunc with the 2025 file.
    """
    con = duckdb.connect(DB_FILE)
    df_new = read_cpi_file(FILE_2025)

    con.execute("DELETE FROM cpi_trunc")
    con.register("df_new", df_new)

    con.execute("""
        INSERT INTO cpi_trunc
        SELECT * FROM df_new
    """)

    con.unregister("df_new")
    con.close()


def load_incremental():
    """
    Update existing dates and insert new dates in cpi_inc.
    """
    con = duckdb.connect(DB_FILE)
    df_new = read_cpi_file(FILE_2025)

    con.register("df_new", df_new)

    con.execute("""
        UPDATE cpi_inc AS old
        SET cpi = new.cpi
        FROM df_new AS new
        WHERE old.date = new.date
    """)

    con.execute("""
        INSERT INTO cpi_inc
        SELECT new.*
        FROM df_new AS new
        LEFT JOIN cpi_inc AS old
          ON new.date = old.date
        WHERE old.date IS NULL
    """)

    con.unregister("df_new")
    con.close()


def show_results():
    con = duckdb.connect(DB_FILE)

    print("\n--- cpi_append sample ---")
    print(con.execute("SELECT * FROM cpi_append LIMIT 10").df())
    print(con.execute("SELECT COUNT(*) AS total_rows FROM cpi_append").df())

    print("\n--- cpi_trunc sample ---")
    print(con.execute("SELECT * FROM cpi_trunc LIMIT 10").df())
    print(con.execute("SELECT COUNT(*) AS total_rows FROM cpi_trunc").df())

    print("\n--- cpi_inc sample ---")
    print(con.execute("SELECT * FROM cpi_inc LIMIT 10").df())
    print(con.execute("SELECT COUNT(*) AS total_rows FROM cpi_inc").df())

    con.close()


if __name__ == "__main__":
    initialize_database()
    load_append()
    load_trunc()
    load_incremental()
    show_results()

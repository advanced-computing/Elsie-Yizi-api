from flask import Flask, request, Response
import pandas as pd
import duckdb

app = Flask(__name__)

DB_PATH = "hate_crimes.db"
TABLE_NAME = "hate_crimes"


def get_connection():
    """Open a connection to the persistent DuckDB database."""
    return duckdb.connect(DB_PATH)


def load_data() -> pd.DataFrame:
    """Load the hate_crimes table from DuckDB."""
    con = get_connection()
    try:
        return con.execute(f"SELECT * FROM {TABLE_NAME}").fetchdf()
    finally:
        con.close()


def safe_int(value, default):
    """Convert value to int safely; fall back to default if invalid."""
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def filter_by_value(data: pd.DataFrame, filterby: str | None, filtervalue: str | None):
    """
    If filterby is provided, filter the DataFrame where data[filterby] == filtervalue
    using case-insensitive string comparison.
    Returns either a DataFrame or (error_message, status_code).
    """
    if not filterby:
        return data

    if filterby not in data.columns:
        return "Invalid filterby column", 400

    if filtervalue is None:
        return "Missing filtervalue", 400

    return data[
        data[filterby].astype(str).str.strip().str.lower()
        == str(filtervalue).strip().lower()
    ]


def apply_limit_offset(data: pd.DataFrame, limit: int, offset: int) -> pd.DataFrame:
    offset = max(offset, 0)
    limit = max(limit, 0)
    return data.iloc[offset : offset + limit]


def convert_to_format(data: pd.DataFrame, fmt: str):
    fmt = (fmt or "json").lower()

    if fmt == "json":
        return Response(data.to_json(orient="records"), mimetype="application/json")

    if fmt == "csv":
        return Response(data.to_csv(index=False), mimetype="text/csv")

    return "Invalid format (use json or csv)", 400


@app.route("/")
def hello_world():
    return "<p>Hello! Try /api/list or /api/columns</p>"


@app.get("/api/columns")
def columns():
    data = load_data()
    return {"columns": data.columns.tolist(), "row_count": int(len(data))}


@app.get("/api/list")
def list_records():
    fmt = request.args.get("format", "json")
    filterby = request.args.get("filterby", None)
    filtervalue = request.args.get("filtervalue", None)

    limit = safe_int(request.args.get("limit", 100), 100)
    offset = safe_int(request.args.get("offset", 0), 0)

    data = load_data()

    data = filter_by_value(data, filterby, filtervalue)
    if isinstance(data, tuple):
        return data

    data = apply_limit_offset(data, limit, offset)

    return convert_to_format(data, fmt)


@app.get("/api/record/<int:idx>")
def get_record(idx: int):
    fmt = request.args.get("format", "json")
    data = load_data()

    if idx < 0 or idx >= len(data):
        return "Record not found", 404

    row = data.iloc[[idx]]
    return convert_to_format(row, fmt)


@app.post("/api/users")
def add_user():
    data = request.json

    username = data.get("username")
    age = data.get("age")
    country = data.get("country")

    if not username or age is None or not country:
        return {"error": "Missing username, age, or country"}, 400

    con = duckdb.connect(DB_PATH)

    con.execute("INSERT INTO users VALUES (?, ?, ?)", [username, age, country])

    con.close()

    return {"message": "User added successfully"}


@app.get("/api/users/stats")
def user_stats():

    con = duckdb.connect(DB_PATH)

    total_users = con.execute("SELECT COUNT(*) FROM users").fetchone()[0]

    avg_age = con.execute("SELECT AVG(age) FROM users").fetchone()[0]

    top_countries = con.execute(
        """
        SELECT country, COUNT(*) as count
        FROM users
        GROUP BY country
        ORDER BY count DESC
        LIMIT 3
        """
    ).fetchall()

    con.close()

    return {
        "total_users": total_users,
        "average_age": avg_age,
        "top_countries": top_countries,
    }


if __name__ == "__main__":
    app.run(debug=True, port=5001)

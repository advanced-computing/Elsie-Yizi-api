from flask import Flask, request, Response
import pandas as pd

app = Flask(__name__)

CSV_PATH = "NYPD_Hate_Crimes_20260213.csv"

def load_data() -> pd.DataFrame:
    """Load the CSV fresh each request (simple + safe for class)."""
    return pd.read_csv(CSV_PATH)


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
        return data  # no filtering requested

    if filterby not in data.columns:
        return "Invalid filterby column", 400

    if filtervalue is None:
        return "Missing filtervalue", 400

    return data[
        data[filterby]
        .astype(str)
        .str.strip()
        .str.lower()
        == str(filtervalue).strip().lower()
    ]


def apply_limit_offset(data: pd.DataFrame, limit: int, offset: int) -> pd.DataFrame:
    offset = max(offset, 0)
    limit = max(limit, 0)
    return data.iloc[offset: offset + limit]


def convert_to_format(data: pd.DataFrame, fmt: str):
    fmt = (fmt or "json").lower()

    if fmt == "json":
        # Return JSON with correct content-type
        return Response(data.to_json(orient="records"), mimetype="application/json")

    if fmt == "csv":
        return Response(data.to_csv(index=False), mimetype="text/csv")

    return "Invalid format (use json or csv)", 400

@app.route("/")
def hello_world():
    return "<p>Hello! Try /api/list or /api/columns</p>"


@app.get("/api/columns")
def columns():
    """See available columns you can use for filterby."""
    data = load_data()
    return {"columns": data.columns.tolist(), "row_count": int(len(data))}


@app.get("/api/list")
def list_records():
    """
    List records with:
      - format=json|csv
      - filterby=<column>&filtervalue=<value>
      - limit=<int>&offset=<int>
    """
    fmt = request.args.get("format", "json")
    filterby = request.args.get("filterby", None)
    filtervalue = request.args.get("filtervalue", None)

    limit = safe_int(request.args.get("limit", 100), 100)
    offset = safe_int(request.args.get("offset", 0), 0)

    data = load_data()

    # Filter (optional)
    data = filter_by_value(data, filterby, filtervalue)
    if isinstance(data, tuple):  # (message, status_code)
        return data

    # Limit/offset
    data = apply_limit_offset(data, limit, offset)

    # Format output
    return convert_to_format(data, fmt)


@app.get("/api/record/<int:idx>")
def get_record(idx: int):
    """Retrieve a single record by row index (identifier) with ?format=json|csv."""
    fmt = request.args.get("format", "json")
    data = load_data()

    if idx < 0 or idx >= len(data):
        return "Record not found", 404

    row = data.iloc[[idx]]  # keep as DataFrame
    return convert_to_format(row, fmt)


if __name__ == "__main__":
    app.run(debug=True, port=5001)

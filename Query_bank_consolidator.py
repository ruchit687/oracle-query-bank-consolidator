"""
Oracle Query-Bank Consolidator
-------------------------------
Reads a list of SQL queries from an Excel-based "query bank" (one query per
row), runs each against an Oracle database, writes each result set to its
own Excel file, then consolidates all outputs into a single deduplicated
summary file.

Useful pattern for: recurring reporting-agency/reference-data extracts where
the set of queries is maintained by an analyst in a spreadsheet rather than
hardcoded in the script.

Requires:
    - Oracle Instant Client installed locally
    - cx_Oracle, pandas, openpyxl

Configuration is read from environment variables (see README) so credentials
are never hardcoded in the script.
"""

import os
import glob
import cx_Oracle
import pandas as pd

# ---------------- CONFIGURATION ----------------
ORACLE_CLIENT_LIB_DIR = os.environ.get("ORACLE_CLIENT_LIB_DIR", r"C:\instantclient_18_5")

DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ.get("DB_PORT", "1521")
DB_SERVICE_NAME = os.environ["DB_SERVICE_NAME"]

QUERY_BANK_PATH = os.environ["QUERY_BANK_PATH"]          # e.g. "queries.xlsx"
QUERY_BANK_SHEET = os.environ["QUERY_BANK_SHEET"]        # e.g. "Region Specific"
QUERY_COLUMN = os.environ.get("QUERY_COLUMN", "SQL query")

OUTPUT_DIR = os.environ.get("OUTPUT_DIR", ".")
SUMMARY_COLUMNS = os.environ.get("SUMMARY_COLUMNS", "AGENCY_NAME,COUNTRY").split(",")
SUMMARY_OUTPUT_NAME = os.environ.get("SUMMARY_OUTPUT_NAME", "summary_output.xlsx")
# ------------------------------------------------

cx_Oracle.init_oracle_client(lib_dir=ORACLE_CLIENT_LIB_DIR)

dsn = f"{DB_HOST}:{DB_PORT}/{DB_SERVICE_NAME}"
con = cx_Oracle.connect(f"{DB_USER}/{DB_PASSWORD}@{dsn}")

# Load the query bank
query_df = pd.read_excel(QUERY_BANK_PATH, sheet_name=QUERY_BANK_SHEET)
queries = list(query_df[QUERY_COLUMN])
filenames = [f"output{i + 1}.xlsx" for i in range(len(queries))]

# Run each query and write its own output file
try:
    for filename, query in zip(filenames, queries):
        query = query.rstrip(query[-1])  # strip trailing separator/char if present
        cursor = con.cursor()
        try:
            cursor.execute(query)
            headers = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
            output_path = os.path.join(OUTPUT_DIR, filename)
            pd.DataFrame(rows, columns=headers).to_excel(output_path, index=False)
        finally:
            cursor.close()
finally:
    con.close()

# Consolidate all per-query output files into a single DataFrame
excel_files = glob.glob(os.path.join(OUTPUT_DIR, "output*.xlsx"))
df_merge = pd.concat(
    (pd.read_excel(f) for f in excel_files),
    ignore_index=True
)

# Extract and deduplicate the summary columns
df_summary = df_merge[SUMMARY_COLUMNS].drop_duplicates()
df_summary.to_excel(os.path.join(OUTPUT_DIR, SUMMARY_OUTPUT_NAME), index=False)
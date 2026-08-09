@echo off
REM ============================================================
REM Environment variable setup for Oracle Query-Bank Consolidator
REM Fill in the values below, then run this script before running
REM query_bank_consolidator.py in the same command prompt session.
REM
REM Note: `set` only affects the current session. For a persistent
REM setting across sessions, use `setx` instead (requires a new
REM terminal window to take effect).
REM ============================================================

set DB_USER=your_db_username
set DB_PASSWORD=your_db_password
set DB_HOST=your_db_host
set DB_PORT=1521
set DB_SERVICE_NAME=your_service_name

set ORACLE_CLIENT_LIB_DIR=C:\instantclient_18_5

set QUERY_BANK_PATH=queries.xlsx
set QUERY_BANK_SHEET=Region Specific
set QUERY_COLUMN=SQL query

set OUTPUT_DIR=.
set SUMMARY_COLUMNS=AGENCY_NAME,COUNTRY
set SUMMARY_OUTPUT_NAME=summary_output.xlsx

echo Environment variables set for this session.
echo Run: python query_bank_consolidator.py
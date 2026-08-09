#!/usr/bin/env bash
# ============================================================
# Environment variable setup for Oracle Query-Bank Consolidator
# Fill in the values below, then source this script before running
# query_bank_consolidator.py in the same shell session:
#
#   source set_env_vars.sh
#
# Note: this must be *sourced*, not executed, or the exports won't
# persist in your current shell.
# ============================================================

export DB_USER="your_db_username"
export DB_PASSWORD="your_db_password"
export DB_HOST="your_db_host"
export DB_PORT="1521"
export DB_SERVICE_NAME="your_service_name"

export ORACLE_CLIENT_LIB_DIR="/opt/oracle/instantclient_18_5"

export QUERY_BANK_PATH="queries.xlsx"
export QUERY_BANK_SHEET="Region Specific"
export QUERY_COLUMN="SQL query"

export OUTPUT_DIR="."
export SUMMARY_COLUMNS="AGENCY_NAME,COUNTRY"
export SUMMARY_OUTPUT_NAME="summary_output.xlsx"

echo "Environment variables set for this session."
echo "Run: python query_bank_consolidator.py"
# Oracle Query-Bank Consolidator

A Python accelerator that runs a batch of SQL queries — maintained in an Excel "query bank" rather than hardcoded — against an Oracle database, and consolidates the results into a single deduplicated summary file.

Useful for recurring reference-data or reporting extracts (e.g. building a list of reporting agencies by country) where an analyst maintains the query list in a spreadsheet and the extraction/consolidation should just run on top of it.

## What it does

1. Connects to an Oracle database via `cx_Oracle` (Oracle Instant Client required).
2. Reads a list of SQL queries from a named sheet/column in an Excel query bank.
3. Executes each query, writing each result set to its own Excel file.
4. Consolidates all per-query output files into a single DataFrame.
5. Extracts and deduplicates a configurable set of summary columns into a final output file.

## Prerequisites

- [Oracle Instant Client](https://www.oracle.com/database/technologies/instant-client.html) installed locally, path configured via `ORACLE_CLIENT_LIB_DIR`.
- Python 3.9+, with `cx_Oracle`, `pandas`, `openpyxl` installed.
- Network access to the Oracle database.
- An Excel "query bank" file with a column of SQL queries.

## Configuration

All configuration is via environment variables — nothing is hardcoded.

| Variable | Required | Description |
|---|---|---|
| `DB_USER` | Yes | Oracle DB username |
| `DB_PASSWORD` | Yes | Oracle DB password |
| `DB_HOST` | Yes | Oracle DB host/IP |
| `DB_PORT` | No (default `1521`) | Oracle DB port |
| `DB_SERVICE_NAME` | Yes | Oracle service name |
| `ORACLE_CLIENT_LIB_DIR` | No (default `C:\instantclient_18_5`) | Path to Oracle Instant Client |
| `QUERY_BANK_PATH` | Yes | Path to the Excel query bank file |
| `QUERY_BANK_SHEET` | Yes | Sheet name containing the queries |
| `QUERY_COLUMN` | No (default `SQL query`) | Column name holding the SQL text |
| `OUTPUT_DIR` | No (default current dir) | Where output files are written |
| `SUMMARY_COLUMNS` | No (default `AGENCY_NAME,COUNTRY`) | Comma-separated columns to keep in the final summary |
| `SUMMARY_OUTPUT_NAME` | No (default `summary_output.xlsx`) | Filename for the final consolidated output |

### Setup scripts

Two helper scripts are included to set these variables — fill in the placeholder values before use:

- **Windows:** `set_env_vars.bat` — sets variables for the current command prompt session.
  ```cmd
  set_env_vars.bat
  python query_bank_consolidator.py
  ```
- **Linux/macOS:** `set_env_vars.sh` — must be *sourced*, not executed, so the exports persist in your shell.
  ```bash
  source set_env_vars.sh
  python query_bank_consolidator.py
  ```

## Scope for improvement

- **Credentials via env vars still land in plaintext in the shell/CI environment** — for production use, pull from a secrets manager (Azure Key Vault, AWS Secrets Manager, etc.) instead.
- **No logging** — currently silent unless something throws. Adding structured logging (query name, row count, duration per query) would make failures much easier to diagnose in a batch of many queries.
- **No retry logic** — a single failed query currently kills the whole run partway through, potentially leaving some `output*.xlsx` files from a prior run mixed in with the current one. Worth clearing/isolating the output directory per run, or writing to a timestamped subfolder.
- **`query.rstrip(query[-1])`** strips whatever the last character happens to be (often a trailing `;`) — fragile if queries don't end consistently. Better to explicitly strip known trailing characters.
- **Single flat "summary columns" extraction is narrow** — could be generalized to support multiple summary views, or a join/aggregation step, rather than a single dedup.
- **Could be parallelized** — queries currently run sequentially; for a large query bank, running them concurrently (with a connection pool) would meaningfully cut runtime.
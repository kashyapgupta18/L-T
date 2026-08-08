"""Chunked batch loader for high-throughput database inserts."""
import sqlite3
import pandas as pd
from typing import Iterator

def chunk_dataframe(df: pd.DataFrame, chunk_size: int = 5000) -> Iterator[pd.DataFrame]:
    for i in range(0, len(df), chunk_size):
        yield df.iloc[i : i + chunk_size]

def load_chunks(df: pd.DataFrame, table_name: str, conn: sqlite3.Connection, chunk_size: int = 5000) -> int:
    total_loaded = 0
    for chunk in chunk_dataframe(df, chunk_size):
        chunk.to_sql(table_name, conn, if_exists="append", index=False)
        total_loaded += len(chunk)
    return total_loaded

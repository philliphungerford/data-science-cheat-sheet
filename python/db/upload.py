import pandas as pd
import urllib
import os
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv

load_dotenv()


def upload_df_to_sqlserver(df, table_name, schema="dbo",
                           if_exists="append", chunksize=1000):

    server = os.getenv("DB_SERVER")
    database = os.getenv("DB_DATABASE")
    uid = os.getenv("DB_UID")
    password = os.getenv("DB_PASSWORD")
    driver = os.getenv("DB_DRIVER")

    params = urllib.parse.quote_plus(
        f"DRIVER={{{driver}}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={uid};"
        f"PWD={password};"
        f"TrustServerCertificate=yes;"
    )

    engine = create_engine(
        f"mssql+pyodbc:///?odbc_connect={params}",
        pool_pre_ping=True
    )
    # --- Validate connection before proceeding ---
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("Database connection successful.")
    except SQLAlchemyError as e:
        print("Database connection failed. Upload aborted.")
        print(f"Error: {e}")
        return

    # --- Upload dataframe ---
    try:
        df.to_sql(
            table_name,
            con=engine,
            schema=schema,
            if_exists=if_exists,
            index=False,
            chunksize=chunksize,
            method="multi"
        )

        print(f"Uploaded {len(df)} rows to {schema}.{table_name}")

    except SQLAlchemyError as e:
        print("Failed to upload dataframe.")
        print(f"Error: {e}")
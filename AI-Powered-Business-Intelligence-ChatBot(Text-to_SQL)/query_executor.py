import pandas as pd
from db_connection import get_connection

def execute_query(sql_query):
    conn = get_connection()
    
    try:
        df = pd.read_sql(sql_query, conn)
        return df
    except Exception as e:
        return str(e)
    finally:
        conn.close()
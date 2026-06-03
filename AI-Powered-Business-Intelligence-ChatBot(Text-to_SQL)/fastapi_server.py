# fastapi_server.py
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd

from text_to_sql import convert_to_sql
from query_executor import execute_query

app = FastAPI(title="Data Chatbot API Engine")

class QueryPayload(BaseModel):
    user_query: str

@app.get("/")
def read_root():
    return {"status": "online", "engine": "Business Intelligence Text-to-SQL Server"}

@app.post("/query")
def process_bi_query(payload: QueryPayload):
    raw_query = payload.user_query
    
    # 1. Generate SQL statement matching keywords
    sql_statement = convert_to_sql(raw_query)
    
    if not sql_statement:
        return {
            "generated_sql": "-- No Match Template Found",
            "is_df": False,
            "result": "Query pattern unrecognized. Try querying 'top 5 products by profit' or 'sales trend by region'."
        }
        
    # 2. Execute query directly against your chatbot_db via pyodbc
    execution_output = execute_query(sql_statement)
    
    # 3. Format result based on type
    if isinstance(execution_output, pd.DataFrame):
        if execution_output.empty:
            return {
                "generated_sql": sql_statement.strip(),
                "is_df": False,
                "result": "The query executed successfully, but returned 0 active data records."
            }
        
        # Structure payload cleanly for the UI table component
        return {
            "generated_sql": sql_statement.strip(),
            "is_df": True,
            "columns": execution_output.columns.tolist(),
            "data": execution_output.values.tolist()
        }
    else:
        # Pass backend execution error strings down gracefully
        return {
            "generated_sql": sql_statement.strip(),
            "is_df": False,
            "result": str(execution_output)
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
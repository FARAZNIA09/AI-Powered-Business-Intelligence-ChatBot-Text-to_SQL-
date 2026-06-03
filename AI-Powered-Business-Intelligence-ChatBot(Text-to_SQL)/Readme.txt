# AI-Powered Business Intelligence Chatbot

An intelligent Text-to-SQL Business Intelligence Chatbot that converts natural language business questions into SQL queries, retrieves data from SQL Server, and displays results through interactive tables and visualizations.

## Project Overview

This project enables users to interact with a business database using plain English queries instead of writing SQL manually.

Examples:

- Top 5 products by sales
- Top 10 products by profit
- Sales by region
- Monthly sales trends

The system automatically:

1. Accepts natural language input
2. Converts text into SQL queries
3. Executes queries on SQL Server
4. Retrieves results using Pandas
5. Displays results in tables
6. Generates visual charts automatically

---

## Features

### User Authentication
- Login System
- Registration System
- User Management

### Text-to-SQL Engine
- Natural Language Query Processing
- SQL Query Generation
- Keyword Matching Engine

### Business Intelligence Dashboard
- Data Visualization
- Interactive Charts
- Query Results Table

### Chart Types
- Bar Chart
- Line Chart
- Histogram

### Query History
- Stores user query history
- Quick query replay

### FastAPI Backend
- REST API Integration
- SQL Execution Layer

---

## Tech Stack

| Technology | Purpose |
|------------|----------|
| Python | Core Programming |
| FastAPI | Backend API |
| SQL Server | Database |
| PyODBC | Database Connection |
| Pandas | Data Processing |
| CustomTkinter | Desktop GUI |
| JSON | User Authentication & History Storage |

---

## Project Architecture

```text
User
 │
 ▼
Desktop Application (CustomTkinter)
 │
 ▼
FastAPI Server
 │
 ▼
Text-to-SQL Engine
 │
 ▼
SQL Server Database
 │
 ▼
Pandas Data Processing
 │
 ▼
Tables + Charts
```

---

## Folder Structure

```text
AI-Powered-Business-Intelligence-Chatbot/
│
├── app.py
├── fastapi_server.py
├── text_to_sql.py
├── query_executor.py
├── db_connection.py
├── config.py
├── utils.py
│
├── users_auth.json
├── chat_history.json
│
├── requirements.txt
│
├── screenshots/
│   ├── login_page.png
│   ├── dashboard.png
│   └── charts.png
│
└── README.md
```

---

# Installation Guide

## Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/AI-Powered-Business-Intelligence-Chatbot.git

cd AI-Powered-Business-Intelligence-Chatbot
```

---

## Step 2: Create Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Step 4: Install SQL Server

Install:

- Microsoft SQL Server
- SQL Server Management Studio (SSMS)

Official Website:

https://www.microsoft.com/en-us/sql-server

---

## Step 5: Create Database

Create a database named:

```sql
CREATE DATABASE chatbot_db;
```

---

## Step 6: Create Required Tables

Example:

```sql
CREATE TABLE Products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100)
);

CREATE TABLE Customers (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100),
    region VARCHAR(100)
);

CREATE TABLE Sales (
    sale_id INT PRIMARY KEY,
    product_id INT,
    customer_id INT,
    revenue FLOAT,
    profit FLOAT,
    sale_date DATE
);
```

---

## Step 7: Insert Sample Data

Add sample business data into:

- Products
- Customers
- Sales

tables.

---

## Step 8: Configure Database Connection

Open:

```python
config.py
```

Update:

```python
DB_CONFIG = {
    "server": "YOUR_SERVER_NAME",
    "database": "chatbot_db",
    "username": "YOUR_USERNAME",
    "password": "YOUR_PASSWORD",
    "driver": "ODBC Driver 17 for SQL Server"
}
```

---

## Step 9: Start FastAPI Server

Open terminal:

```bash
python fastapi_server.py
```

Expected Output:

```text
Uvicorn running on:

http://127.0.0.1:8000
```

Check API:

```text
http://127.0.0.1:8000
```

---

## Step 10: Launch Application

Open another terminal:

```bash
python app.py
```

The desktop application will start.

---

# Demo Login Credentials

```text
Username: admin
Password: admin123
```

---

# Example Queries

```text
Top 5 products by sales

Top 10 products by profit

Sales by region

Monthly sales trend

Revenue by region

Best products by revenue
```

---

# API Endpoint

## POST Request

```http
POST /query
```

Request:

```json
{
  "user_query": "Top 5 products by sales"
}
```

Response:

```json
{
  "generated_sql": "SELECT TOP 5 ...",
  "is_df": true,
  "columns": [...],
  "data": [...]
}
```

---

# Future Enhancements

- OpenAI Integration
- Gemini API Integration
- LangChain Integration
- LLM-based Text-to-SQL
- Role-Based Authentication
- Export Reports to PDF
- Dashboard Analytics
- Cloud Deployment
- Voice Assistant Support

---

# Screenshots

Add screenshots here:

### Login Screen

![Login](screenshots/login_page.png)

### Dashboard

![Dashboard](screenshots/dashboard.png)

### Charts

![Charts](screenshots/charts.png)

---

# Author

Faraz Niyazi

B.Tech Computer Science Engineering

AI | Data Analytics | Business Intelligence | Machine Learning

---

# License

This project is developed for educational and portfolio purposes.
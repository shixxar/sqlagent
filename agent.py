import os
import sqlite3
import pandas as pd
import logging
from typing import AsyncGenerator
from typing_extensions import override
from dotenv import load_dotenv
import shutil

from google.adk.agents import LlmAgent, BaseAgent, SequentialAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.adk.events import Event
from litellm import completion
import litellm
from google.adk.models.lite_llm import LiteLlm
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
DB_URL = "https://storage.googleapis.com/benchmarks-artifacts/chinook/Chinook.db"
DB_PATH = "Chinook.db"
LOCAL_DB_PATH = r"\\C:\Users\rkshi\sql\Chinook.db"  # Path to your local Chinook.db file

API_KEY = os.getenv("GROQ_API_KEY")

# Database schema
db_schema = '''
## Tables and Relationships

### **Customer**
- **CustomerId** (PK)
- FirstName
- LastName
- Company
- Address
- City
- State
- Country
- PostalCode
- Phone
- Fax
- Email
- SupportRepId → (FK to Employee.EmployeeId)

---

### **Employee**
- **EmployeeId** (PK)
- LastName
- FirstName
- Title
- ReportsTo → (FK to Employee.EmployeeId)
- BirthDate
- HireDate
- Address
- City
- State
- Country
- PostalCode
- Phone
- Fax
- Email

---

### **Invoice**
- **InvoiceId** (PK)
- CustomerId → (FK to Customer.CustomerId)
- InvoiceDate
- BillingAddress
- BillingCity
- BillingState
- BillingCountry
- BillingPostalCode
- Total

---

### **InvoiceLine**
- **InvoiceLineId** (PK)
- InvoiceId → (FK to Invoice.InvoiceId)
- TrackId → (FK to Track.TrackId)
- UnitPrice
- Quantity

---

### **Track**
- **TrackId** (PK)
- Name
- AlbumId → (FK to Album.AlbumId)
- MediaTypeId → (FK to MediaType.MediaTypeId)
- GenreId → (FK to Genre.GenreId)
- Composer
- Milliseconds
- Bytes
- UnitPrice

---

### **Album**
- **AlbumId** (PK)
- Title
- ArtistId → (FK to Artist.ArtistId)

---

### **Artist**
- **ArtistId** (PK)
- Name

---

### **Genre**
- **GenreId** (PK)
- Name

---

### **MediaType**
- **MediaTypeId** (PK)
- Name

---

### **PlaylistTrack**
- **PlaylistId** → (FK to Playlist.PlaylistId)
- **TrackId** → (FK to Track.TrackId)

---

### **Playlist**
- **PlaylistId** (PK)
- Name

---

## **Relationships**
- **Customer (1) → (∞) Invoice**
- **Invoice (1) → (∞) InvoiceLine**
- **InvoiceLine (∞) ← (1) Track**
- **Track (∞) → (1) Album**
- **Track (∞) → (1) MediaType**
- **Track (∞) → (1) Genre**
- **Album (∞) → (1) Artist**
- **Track (∞) → (∞) Playlist (via PlaylistTrack)**
- **Employee (1) → (∞) Customer (as SupportRepId)**
- **Employee (1) → (∞) Employee (as ReportsTo)**
'''

# Function to copy the database from the local path
def setup_database():
    if not os.path.exists(DB_PATH):
        if os.path.exists(LOCAL_DB_PATH):
            shutil.copyfile(LOCAL_DB_PATH, DB_PATH)
            logger.info(f"Database copied from {LOCAL_DB_PATH} to {DB_PATH} successfully.")
        else:
            logger.error(f"Local database not found at {LOCAL_DB_PATH}. Please ensure the path is correct.")
            exit()

# Function to connect to the database
def connect_db():
    return sqlite3.connect(DB_PATH)

# Agent to generate SQL query from natural language question
sql_generator_agent = LlmAgent(
    model=LiteLlm(model="groq/llama3-70b-8192"),
    name="sql_agent",
    instruction=f"""
You are an expert SQL query generator. Convert natural language questions into precise SQL queries for a SQLite database. The database schema is as follows:

{db_schema}

Generate ONLY the SQL query without any explanation, comments, or markdown formatting.
Do not output "Here is the SQL query:" or similar text. Generate just the raw SQL code.
""",
    output_key="sql_query",
)

# Agent to execute SQL query and store results
class SQLExecutorAgent(BaseAgent):
    @override
    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        sql_query = ctx.session.state.get("sql_query", "")
        if not sql_query:
            yield Event.message("No SQL query found in session state.")
            return

        # Log the SQL query for debugging
        logger.info(f"Executing SQL query: {sql_query}")
        
        # Ensure database is set up
        setup_database()
        
        conn = connect_db()
        try:
            # Execute the query
            results = pd.read_sql_query(sql_query, conn)
            logger.info(results)
            
            # Store the results
            if not results.empty:
                ctx.session.state["query_results"] = results.to_dict(orient="records")
                ctx.session.state["results_df"] = results
                
                # Don't yield a message here - just log it
                logger.info(f"Query executed successfully. Found {len(results)} results.")
            else:
                ctx.session.state["query_results"] = []
                ctx.session.state["results_df"] = pd.DataFrame()
                logger.info("Query executed successfully but returned no results.")
        except sqlite3.Error as e:
            error_msg = f"Database error: {e}"
            logger.error(error_msg)
            ctx.session.state["query_results"] = []
            ctx.session.state["results_df"] = pd.DataFrame()
            yield Event.message(error_msg)
        finally:
            conn.close()
globe_result=""
# Agent to format and present the query results
class ResultFormatterAgent(BaseAgent):
    @override
    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        results_df = ctx.session.state.get("results_df")
        sql_query = ctx.session.state.get("sql_query", "")
        global globe_result
        if results_df is None or results_df.empty:
            yield Event.message("No results to display for your query.")
            return
        logger.info("1,2,3,4")
        logger.info(results_df)
        # Format the results as a readable table
        table_str = results_df.to_string(index=False)
        
        # Store both the query and formatted results in the session state
        # but only the formatted results will be displayed to the user
        ctx.session.state["sql_query_used"] = sql_query  # Store for internal use
        ctx.session.state["formatted_result"] = table_str
        globe_result=table_str
        # Only log the SQL query (for debugging), don't show it to the user
        logger.info(f"SQL Query Used: {sql_query}")
        
        # Don't yield a message here, as we want the response agent to handle the final output

# Final agent to combine information for a complete response
response_agent = LlmAgent(
    name="ResponseAgent",
    model=LiteLlm(model="groq/llama3-70b-8192"),
    instruction=f"""
You are a helpful database assistant. Provide a clear and concise response based on the SQL query results which is {globe_result}.
Your response should focus ONLY on:
1. The results of the query (already formatted as a table)
2. A brief, clear explanation of what these results mean in relation to the user's question

DO NOT include the SQL query itself in your response. The user only wants to see the results and an explanation.
Use natural language to explain the findings from the query in a way that directly answers the user's question.

Keep your response focused on the data and avoid unnecessary elaboration.
""",
    output_key="final_response",
)

# Sequential agent to orchestrate the workflow
query_pipeline = SequentialAgent(
    name="QueryPipeline",
    sub_agents=[
        sql_generator_agent,
        SQLExecutorAgent(name="SQLExecutorAgent"),
        ResultFormatterAgent(name="ResultFormatterAgent"),
        response_agent,
    ],
)

# Initialize the database
setup_database()

# Set this as the root agent
root_agent = query_pipeline

# Example code to run the agent
# Create a session service
session_service = InMemorySessionService()

# Create a runner - fix the initialization with required app_name
runner = Runner(
    agent=root_agent, 
    session_service=session_service,
    app_name="ChinookDatabaseAgent"  # Adding the required app_name parameter
)

# Run the agent with a user query
async def run_query(user_query):
    session_id = "example_session"
    response = await runner.run_async(session_id=session_id, user_input=user_query)
    return response

# Example usage
import asyncio

async def main():
    user_query = "Show me the top 5 customers by total purchase amount"
    response = await run_query(user_query)
    print(response)

if __name__ == "__main__":
    asyncio.run(main())
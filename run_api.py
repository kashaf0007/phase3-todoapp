"""
Simple test to run the FastAPI application
"""
import uvicorn
import os

if __name__ == "__main__":
    # Set the DATABASE_URL if not already set
    if not os.getenv("DATABASE_URL"):
        os.environ["DATABASE_URL"] = "postgresql://neondb_owner:npg_TktC9FJmPig5@ep-autumn-recipe-ade5hdh4-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
    
    print("Starting the FastAPI application...")
    print("You can test the API at http://127.0.0.1:8000")
    print("API documentation available at http://127.0.0.1:8000/docs")
    
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
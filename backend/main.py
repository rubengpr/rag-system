"""
Main Entry Point

This module serves as the entry point for the FastAPI application.
It imports the configured app from app.py and runs the server.
"""

from app import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

"""
Run Module

This module serves as the entry point for starting the FastAPI application server.

The __name__ == "__main__" pattern ensures that the server only starts when this
file is executed directly, not when it's imported as a module in other files.

Example:
    Direct execution (server starts):
        $ python run.py
        INFO: Uvicorn running on http://0.0.0.0:8000
    
    Import in another file (server doesn't start):
        >>> from run import app  # Server won't start, just imports app
        >>> # Can use 'app' for testing or other purposes
"""

import uvicorn
import os
from dotenv import load_dotenv

# Load local enviroment variables
load_dotenv()

# Get enviroment settings - os.getenv returns strings
DEBUG = os.getenv("DEBUG", "False")


if __name__ == "__main__":
    """
    Entry point guard.
    
    This block only executes when run.py is the main program.
    Prevents the server from starting when run.py is imported elsewhere.
    
    How it works:
        - When executed: python run.py
          __name__ == "__main__" → True → Server starts
        
        - When imported: from run import app
          __name__ == "run" → False → Server doesn't start
    """
    if DEBUG == "True":
        print("Starting FastAPI server in DEVELOPMENT mode (hot reload enabled)...")
        uvicorn.run(
            "main:app", 
            host="localhost", 
            port=8000,
            reload=True,
            log_level="debug"
        )
    else:
        print("Starting FastAPI server in PRODUCTION mode...")
        uvicorn.run(
            "main:app", 
            host="localhost", 
            port=8000,
            reload=False,
            log_level="info"
        )
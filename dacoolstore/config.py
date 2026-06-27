import os

try:
    from dotenv import load_dotenv

    # Load .env file from the current directory or parent directories
    load_dotenv()
except ImportError:
    pass

# Database configuration with defaults matching original code
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "######")
DB_NAME = os.getenv("DB_NAME", "dacoolstore")

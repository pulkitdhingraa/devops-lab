# Define a custom exception class DatabaseConnectionError. Then write a function connect_to_db(host, port, db_name) that:
# - Raises DatabaseConnectionError (not a generic Exception) if host is empty or port is not in 1-65535
# - Raises DatabaseConnectionError with a descriptive message if the connection attempt fails
# - Uses raise ... from e to preserve the original error chain

# You can mock the actual connection with: import psycopg2

import psycopg2

class DatabaseConnectionError(Exception):
    pass

def connect_to_db(host: str, port: int, db_name: str):
    errors = []
    if not host:
        errors.append("Host cannot be empty")
    if not (1 <= port <= 65535):
        errors.append(f"Port {port} is out of range (1-65535)")
    if errors:
        raise DatabaseConnectionError(", ".join(errors))    
    try:
        conn = psycopg2.connect(host=host, port=port, dbname=db_name)
        return conn
    except psycopg2.OperationalError as e:
        raise DatabaseConnectionError(f"Could not connect to {host}:{port}/{db_name}") from e
    

# Key Learnings

# Collect all missing invalid input before raising
# Wrap in domain exception with context
# Use from e to preserve the chain
# Never return None on failure raise instead
# TiDB Reader Service

A production-ready FastAPI service that provides a read-only REST API over a TiDB (MySQL-compatible) `users` table.

## Features

- **FastAPI** with synchronous endpoints
- **OpenAPI 3.0.3** specification
- **Connection pooling** for optimal performance
- **Parameterized SQL** queries for security
- **Environment-based configuration**
- **Comprehensive error handling**
- **Production-ready logging**

## API Endpoints

### GET /users/{id}
Retrieve a user by ID from the `users` table.

**Response:**
- `200 OK`: Returns user data as JSON object with all columns
- `404 Not Found`: User not found
- `500 Internal Server Error`: Database or server error

## Environment Variables

Configure the following environment variables before running the service:

```bash
TIDB_HOST=your-tidb-host          # Default: localhost
TIDB_PORT=4000                    # Default: 4000
TIDB_USER=your-username           # Default: root
TIDB_PASSWORD=your-password       # Default: (empty)
TIDB_DATABASE=your-database       # Default: test
TIDB_SSL_MODE=PREFERRED           # Default: PREFERRED
POOL_SIZE=10                      # Default: 10
MAX_OVERFLOW=20                   # Default: 20
```

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Unix/macOS:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Service

### Development Mode

```bash
# Set environment variables (example)
set TIDB_HOST=gateway01.us-west-2.prod.aws.tidbcloud.com
set TIDB_PORT=4000
set TIDB_USER=your-username
set TIDB_PASSWORD=your-password
set TIDB_DATABASE=your-database

# Run the service
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
# Set environment variables
export TIDB_HOST=your-tidb-host
export TIDB_PORT=4000
export TIDB_USER=your-username
export TIDB_PASSWORD=your-password
export TIDB_DATABASE=your-database

# Run with production settings
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Testing the API

Once the service is running, you can test it:

1. **Health check:**
   ```bash
   curl http://localhost:8000/
   ```

2. **Get user by ID:**
   ```bash
   curl http://localhost:8000/users/1
   ```

3. **OpenAPI documentation:**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc
   - OpenAPI JSON: http://localhost:8000/openapi.json

## Database Schema

The service expects a `users` table in your TiDB database. The service will return all columns present in the table as JSON objects.

Example table structure:
```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

## Security Features

- **Read-only access**: Only SELECT queries are executed
- **Parameterized queries**: Prevents SQL injection attacks
- **No credential exposure**: Database errors don't leak sensitive information
- **SSL/TLS support**: Configurable SSL mode for secure connections

## Architecture

```
├── src/
│   ├── main.py          # FastAPI application and routes
│   ├── config.py        # Environment configuration
│   ├── db.py           # Database connection pool
│   ├── repository.py   # Data access layer
│   └── service.py      # Business logic layer
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Logging

The service provides comprehensive logging for:
- Database connection events
- API requests and responses
- Error conditions
- Application lifecycle events

Logs are formatted with timestamps and log levels for production monitoring.

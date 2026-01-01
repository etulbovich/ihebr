# Goal
Generate a production-style Python SYNC service that exposes a read-only REST API over a TiDB (MySQL-compatible) table `users`.

# Tech stack
- FastAPI (sync endpoints)
- Uvicorn to run
- MySQL driver (sync): prefer mysql-connector-python
- No ORM. Use parameterized SQL only.

# OpenAPI requirement
- The service must expose OpenAPI 3.0.x.
- Set FastAPI app openapi_version="3.0.3".

# Database rules (security + correctness)
- Read-only access only (SELECT). Never generate INSERT/UPDATE/DELETE/DDL.
- Parameterize all queries (no string concatenation).
- Always apply LIMIT for list endpoints and support pagination (limit, offset).
- Use a connection pool.
- Credentials and connection parameters must come only from environment variables.
- Enable TLS/SSL in the connection config when supported.

# API requirements
- Implement:
  - GET /users/{id}
- Return all columns from `users`.
- If schema is unknown at codegen time, fetch rows as dict using cursor description and return JSON objects.

# Project structure
- src/
  - main.py (FastAPI app + routers)
  - db.py (pool + get_connection)
  - repository.py (SQL for users)
  - service.py (business wrapper)
  - config.py (env config)
- Include requirements.txt and a short README with run instructions.

# Error handling
- For not found: 404
- For DB errors: 500 (do not leak secrets)
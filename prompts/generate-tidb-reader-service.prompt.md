Generate a Python 3.11+ SYNC FastAPI service that reads from TiDB (MySQL-compatible) using mysql-connector-python.

Table:
- name: users
- primary key: id
Return:
- all columns

Endpoints:
1) GET /users/{id}
   - Query: SELECT * FROM users WHERE id = %s
   - If not found: return 404

Implementation constraints:
- Use connection pooling (mysql.connector.pooling.MySQLConnectionPool).
- Use environment variables for DB config:
  TIDB_HOST, TIDB_PORT, TIDB_USER, TIDB_PASSWORD, TIDB_DATABASE, TIDB_SSL_MODE
- Never hardcode credentials.
- Parameterized SQL only.
- Return rows as JSON dicts even if schema is unknown:
  use cursor.description to map column names to values.

OpenAPI:
- Must be OpenAPI 3.0.3 (FastAPI app openapi_version="3.0.3")
- Response schema can be generic (object with additionalProperties: true) because we return all columns.

Deliverables:
- Create files: src/config.py, src/db.py, src/repository.py, src/service.py, src/main.py
- Add requirements.txt and README.md with run steps.
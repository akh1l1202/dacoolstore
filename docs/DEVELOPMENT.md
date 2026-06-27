# Developer Guide - Da Cool Store

This guide details the instructions for developers contributing to the **Da Cool Store** repository.

---

## 🛠️ Environment Setup

### Prerequisites
1.  Python 3.9+ installed on your host.
2.  MySQL Server running (version 8.0+ recommended) or Docker installed.

### Development Installation
Set up your virtual environment and install the package in editable mode:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -e ".[dev]"
```

Editable installation (`-e`) installs the package locally, allowing you to import `dacoolstore` anywhere while reflecting local code changes instantly.

---

## 💅 Coding Standards & Style

The project enforces PEP 8 and modern Python patterns. Linting and formatting are managed by **Ruff**.

### Line Length
Line lengths are configured to **120 characters** in `pyproject.toml`.

### Imports Ordering
Imports should follow:
1. Standard library imports
2. Third-party imports (e.g. `PySimpleGUI`, `mysql`)
3. Project source package imports (e.g. `dacoolstore.database`)

### SQL Queries
All database query statements must use parameterized placeholders (`%s`) to block SQL Injection vulnerabilities:
```python
# CORRECT:
cursor.execute("SELECT * FROM customers WHERE Cust_PhoneNumber=%s;", (phone,))

# INCORRECT (Never construct SQL queries using string formatting):
cursor.execute(f"SELECT * FROM customers WHERE Cust_PhoneNumber='{phone}';")
```

---

## 🧪 Running Tests

Tests are placed in the `tests/` folder. We use `pytest` for unit testing.

To execute tests:
```bash
pytest
```

To run lint checks:
```bash
ruff check .
```

To automatically resolve fixable linting errors:
```bash
ruff check . --fix
```

---

## 🐳 Docker Container Operations

### Spinning up local Database
Start the MySQL database service locally:
```bash
docker compose up -d
```

### Stopping Database
Shut down the MySQL service and purge container instances:
```bash
docker compose down
```

To purge volumes (including data in tables):
```bash
docker compose down -v
```

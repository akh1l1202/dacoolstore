# Da Cool Store 🛒

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Code Style: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?logo=docker&logoColor=white)](https://www.docker.com/)

An interactive desktop-based store management system built with Python, PySimpleGUI, and MySQL. It features a complete customer checkout interface alongside a robust administrative panel for managing products, categories, employee attendance, and order fulfillment.

---

## 📖 Table of Contents

1. [Project Overview](#-project-overview)
2. [Motivation](#-motivation)
3. [Features](#-features)
4. [Screenshots](#-screenshots)
5. [Architecture](#-architecture)
6. [Folder Structure](#-folder-structure)
7. [Tech Stack](#-tech-stack)
8. [Requirements](#-requirements)
9. [Installation & Setup](#-installation--setup)
10. [Configuration](#-configuration)
11. [Running the Project](#-running-the-project)
12. [Database Setup & Sample Data](#-database-setup--sample-data)
13. [Usage Guide](#-usage-guide)
14. [Testing Suite](#-testing-suite)
15. [Future Improvements](#-future-improvements)
16. [Known Limitations](#-known-limitations)
17. [Contributing](#-contributing)
18. [License](#-license)
19. [Author](#-author)

---

## 🌟 Project Overview

**Da Cool Store** is designed to demonstrate clean desktop-application architecture in Python. It splits users into two interfaces:
*   **Customer Workspace**: Register, log in, browse product catalogs dynamically loaded by category, build shopping carts, calculate invoice totals, and trace past order history.
*   **Staff/Admin Workspace**: Record staff attendance, view employee rosters, add/delete products and categories, and track/update the delivery status of customer orders.

---

## 💡 Motivation

This project has been modernized from a legacy script structure to:
1.  Eliminate circular dependencies and recursive window loops common in simple PySimpleGUI projects.
2.  Implement secure industry-standard credential handling (PBKDF2-HMAC-SHA256 password hashing).
3.  Support modern configuration management (`.env` integration).
4.  Provide robust database session management, preventing cursor/connection leaks.
5.  Introduce full test coverage (using `pytest`) and modern tooling (`ruff`).

---

## ⚡ Features

### Customer Features
*   **Secure Authentication**: Accounts protected with PBKDF2-HMAC-SHA256 password hashing.
*   **Interactive Shopping**: Browse products grouped by categories and view invoice totals dynamically in a billing sub-panel.
*   **Order Fulfillment History**: Track past order records and verify delivery status using phone numbers.

### Staff & Admin Features
*   **Staff Registry & Logging**: Track employee attendance registry logs.
*   **Catalog Control**: Complete CRUD interfaces to add or retire categories and products.
*   **Order Management**: View and modify shipping delivery statuses.

---

## 📸 Screenshots

### Welcome Screen
![Welcome Screen](https://github.com/user-attachments/assets/3c487260-9e36-4849-9add-781c310d16c1)

### Customer Registration & Login
![Customer Registration](https://github.com/user-attachments/assets/27ba08ce-e573-4fac-a72f-9c293a869a49)

### Staff Administration Panel
![Staff Login](https://github.com/user-attachments/assets/95a9dc39-192c-4225-8f03-ad04fa9a3e00)

---

## 🏗️ Architecture

The project utilizes a modular package design:
*   **`main.py`**: Serves as the central event controller routing control flows between windows sequentially, resolving the call-stack overflow issue of the legacy code.
*   **`database.py`**: Encapsulates DB-API connections. Employs defensive checks and context cleanups to block leaks.
*   **`security.py`**: Manages credential security with salted PBKDF2 hashing, including an automatic plain-text fallback checker for legacy databases.
*   **`config.py`**: Manages configuration parsing via environment variables.

For details, check out [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

---

## 📂 Folder Structure

```directory
da-cool-store/
├── .github/                   # GitHub templates & CI pipelines
├── dacoolstore/               # Source package
│   ├── assets/                # Media assets (icons, images)
│   │   └── meow.png
│   ├── __init__.py
│   ├── __main__.py            # Module entrypoint (python -m dacoolstore)
│   ├── admin.py               # Administrator GUI layout & actions
│   ├── config.py              # Configuration manager
│   ├── customer.py            # Customer GUI layout & actions
│   ├── database.py            # Database tables setup & queries
│   ├── main.py                # Main window orchestrator
│   ├── security.py            # Cryptographic password hashing
│   └── staff.py               # Staff member GUI layout & actions
├── docs/                      # Architectural & developer manuals
│   ├── ARCHITECTURE.md
│   ├── DATABASE.md
│   └── DEVELOPMENT.md
├── tests/                     # pytest automated tests suite
│   ├── test_config.py
│   ├── test_database.py
│   └── test_security.py
├── .env.example               # Config environment template
├── .gitignore
├── CODE_OF_CONDUCT.md
├── docker-compose.yml         # Dev database compose file
├── Dockerfile                 # Application packaging
├── LICENSE                    # MIT license details
├── pyproject.toml             # Packaging metadata & ruff config
└── requirements.txt           # Dependency requirements list
```

---

## 🛠️ Tech Stack

*   **Language**: Python 3.9+
*   **UI Framework**: PySimpleGUI (v4)
*   **Database**: MySQL Server 8+
*   **Testing**: pytest
*   **Linting/Formatting**: Ruff
*   **Deployment**: Docker & Docker Compose

---

## 📋 Requirements

*   Python 3.9, 3.10, 3.11, or 3.12
*   A running MySQL Server instance (local or via Docker Compose)
*   For Linux hosts, standard Tkinter development libraries (`sudo apt install python3-tk`) are required.

---

## 🚀 Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/akh1l1202/dacoolstore.git
cd dacoolstore
```

### 2. Set up Virtual Environment
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
# Alternatively, install in editable mode
pip install -e .
```

---

## ⚙️ Configuration

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` and fill in your MySQL server details:
   ```env
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=your_actual_mysql_password
   DB_NAME=dacoolstore
   ```

---

## 💾 Database Setup & Sample Data

You can start a local pre-configured MySQL instance using Docker:
```bash
docker compose up -d
```
This spins up a MySQL container listening on `localhost:3306`. 

Alternatively, if you run a local MySQL installation, ensure a database named `dacoolstore` exists. Upon first launch of the application, **all tables will be automatically initialized and populated with demo records**.

---

## 🏃 Running the Project

Run the application as a Python module:
```bash
python -m dacoolstore
```
If you installed the package using `pip install -e .`, you can launch it from anywhere simply by running:
```bash
dacoolstore
```

---

## 🧪 Testing Suite

Tests are managed using `pytest`. Run them with:
```bash
pytest
```
To run tests with code formatting checks:
```bash
ruff check .
```

---

## 🔮 Future Improvements

1.  **GUI modernizations**: Migrate from PySimpleGUI v4 to a more modern framework like CustomTkinter or PySide6 for contemporary UI design.
2.  **API Backend**: Decouple database calls from UI code using a RESTful or gRPC API server.
3.  **Analytics Dashboard**: Visual charts for staff to analyze sales trends and customer registration trends.

---

## ⚠️ Known Limitations

*   **GUI over SSH**: Running the GUI inside Docker requires X11 session forwarding, which can be complex depending on host OS. It is recommended to run the database in Docker and the application locally on the host.
*   **Database Migrations**: Schema alterations currently require manual SQL operations. Integrating alembic-like structures is planned.

---

## 🤝 Contributing

Contributions are welcome! Please read [DEVELOPMENT.md](docs/DEVELOPMENT.md) to understand coding styles, testing, and pull request processes.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## ✍️ Author

*   **Akhil Tyagi** - *Initial Work & Modernization*
*   Email: [tyagi.akhil1202@gmail.com](mailto:tyagi.akhil1202@gmail.com)
*   GitHub: [@akh1l1202](https://github.com/akh1l1202)

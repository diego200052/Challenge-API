# Challenge API

This project is an API developed with **FastAPI** to manage bank accounts, payments, and expenses. It provides endpoints to create, read, update, and delete information related to these entities.

## Table of Contents

- [Challenge API](#challenge-api)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Requirements](#requirements)
  - [Installation](#installation)
  - [Licence](#licence)

## Features

- **Bank Account Management**:
  - Create accounts.
  - Check balances.
  - Update account information.
  - Delete accounts.
- **Payment Management**:
  - Create payments.
  - Approve, cancel, and execute payments.
- **Expense Management**:
  - Register and update expenses.
  - Generate payments linked to approved expenses.

## Requirements

- Python 3.12 or higher.
- PostgreSQL.
- Poetry for dependency management.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/diego200052/Challenge-API
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv env
   source env/bin/activate
3. Install dependencies:
   ```bash
   pip install poetry
   poetry install
4. Run database migrations:
   ```bash
   alembic upgrade head
5. Configure environment variables:
    ```bash
    DATABASE_PORT
    DATABASE_USER
    DATABASE_PASSWORD
    DATABASE_NAME
    DATABASE_HOST
    DATABASE_HOSTNAME
    ACTUAL_TIMEZONE
    CLIENT_ORIGIN
1. Start the server:
   ```bash
   sh run.sh
## Licence

**Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)**

You are free to:
- Share — copy and redistribute the material in any medium or format.
- Adapt — remix, transform, and build upon the material.

Under the following terms:
- Attribution — You must give appropriate credit, provide a link to the license, and indicate if changes were made.
- NonCommercial — You may not use the material for commercial purposes.

Full license text: https://creativecommons.org/licenses/by-nc/4.0/legalcode

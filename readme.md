# Inventory Management System

An inventory management system built with Django for managing products, suppliers, categories, stock transactions, and other business workflows.

## Project Overview

This inventory management system allows users to:

- Manage categories, suppliers, and products.
- Track stock transactions (add or remove stock).
- View dashboards with insights (low stock, recent transactions, etc.).
- Perform filtering and searching on stock transactions.

## Getting Started

Follow the steps below to set up and run the project on your local machine.

### Prerequisites

Ensure you have the following installed on your system:

1. **Python** (Version 3.10 or above recommended)
2. **Django** (Version 5.1.3)
3. **SQLite** (default database included with Django)
4. **Git** (to clone the repository)

### Installation Steps

1. **Clone the repository**:

  ```bash
  git clone https://github.com/jaydeepravaliya/inventory_management_system.git
  ```

2. **Navigate to the project directory**:

  ```bash
  cd inventory_management_system
  ```

3. **Set up a virtual environment (optional but recommended)**:

  ```bash
  python -m venv venv
  source venv/bin/activate # On Windows: venv\Scripts\activate
  ```

4. **Install required packages**:

```bash
pip install -r requirements.txt
```

### Database Setup

1. **Apply database migrations**: Run the following commands to set up the database schema:

  ```bash
  python manage.py makemigrations
  python manage.py migrate
  ```

2. **Create a superuser**: This user will have admin privileges to access the Django Admin panel.

```bash
python manage.py createsuperuser
```

1. **Populate the database with dummy data (optional)**: If you want to quickly populate the database with sample data for testing, run the following command:

```bash
python manage.py populate_db
```

# Inventory Management System

An inventory management system built with Django for managing products, suppliers, categories, stock transactions, and other business workflows.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Getting Started](#getting-started)

  - [Prerequisites](#prerequisites)
  - [Installation Steps](#installation-steps)
  - [Database Setup](#database-setup)

3. [Workflow and Usage](#workflow-and-usage)

  - [Creating Categories](#1-creating-categories)
  - [Adding Suppliers](#2-adding-suppliers)
  - [Adding Products](#3-adding-products)
  - [Stock Transactions](#4-stock-transactions)
  - [Dashboard Insights](#5-dashboard-insights)

4. [Screenshots](#screenshots)
5. [Additional Information](#additional-information)

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

1. **Apply database migrations:**
Run the following commands to set up the database schema:

  ```bash
  python manage.py makemigrations
  python manage.py migrate
  ```

2. **Create a superuser:** 
This user will have admin privileges to access the Django Admin panel.

```bash
python manage.py createsuperuser
```

1. **Populate the database with dummy data (optional):**
If you want to quickly populate the database with sample data for testing, run the following command:

```bash
python manage.py populate_db
```

### Workflow and Usage

#### 1\. **Creating Categories**

- Navigate to the **Categories** section from the dashboard.
- Add categories such as _Beverages_, _Snacks_, etc.
- **Note**: Categories are required to classify products.

#### 2\. **Adding Suppliers**

- Navigate to the **Suppliers** section from the dashboard.
- Add supplier information, including _name_, _email_, and _phone number_.
- **Note**: Suppliers are required to associate with products.

#### 3\. **Adding Products**

- Navigate to the **Products** section from the dashboard.
- Add product details, including _name_, _category_, _supplier_, _price_, and _initial stock level_.
- **Note**: Both categories and suppliers must be created before adding products.

#### 4\. **Stock Transactions**

- Go to the **Stock Transactions** page.
- Use the "Add Stock Transaction" button to manage inventory.

  - **Transaction Types**: Add stock or Remove stock.
  - View available stock while adding/removing.
  - Ensure not to remove more stock than available.

- Transactions can be searched and filtered by:

  - Transaction Type (Add/Remove).
  - Product Name.
  - Performed By.
  - Date Range.

#### 5\. **Dashboard Insights**

- The dashboard provides insights into:

  - Total stock items.
  - Recently added/removed stock.
  - Low stock products.
  - Charts showing stock movements and category breakdown.

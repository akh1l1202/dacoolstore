# Database Schema Documentation - Da Cool Store

This document outlines the database schema, table columns, and data relationships for the **Da Cool Store** application.

---

## 📊 Database Schema Entity-Relationship Map

```mermaid
erDiagram
    customers ||--o{ orders : "places"
    categories ||--o{ products : "contains"
    staff ||--o{ attendance : "records"

    customers {
        int Cust_ID PK "AUTO_INCREMENT"
        varchar(255) Cust_Name
        tinytext Cust_Gender
        varchar(255) Cust_EmailAddress
        varchar(15) Cust_PhoneNumber UK
        varchar(200) Cust_Password "PBKDF2 Hashed"
    }

    orders {
        int OrderID PK "AUTO_INCREMENT"
        varchar(15) Cust_PhoneNumber FK
        varchar(500) Cust_HomeAddress
        varchar(500) Note
        timestamp Time "DEFAULT CURRENT_TIMESTAMP"
        varchar(50) Delivery_Status "DEFAULT 'Not Delivered'"
    }

    categories {
        int CategoryID PK
        varchar(255) CategoryName
    }

    products {
        int ProductID PK "AUTO_INCREMENT"
        varchar(255) ProductName
        decimal(10-2) Price
        int CategoryID FK
    }

    staff {
        int Staff_ID PK "AUTO_INCREMENT"
        varchar(50) Staff_Name
        char(40) Staff_Post
        enum Gender "Male, Female, Other"
        varchar(255) Password "PBKDF2 Hashed"
    }

    attendance {
        int attendanceid PK "AUTO_INCREMENT"
        int staffid "DEFAULT NULL"
        varchar(255) staffname "DEFAULT NULL"
        timestamp timestamp "DEFAULT CURRENT_TIMESTAMP"
    }
```

---

## 🗄️ Tables Specification

### 1. `customers`
Stores customer registration profiles.
*   `Cust_PhoneNumber` is enforced as unique and serves as the key for linking orders and looking up user logins.
*   `Cust_Password` stores PBKDF2-HMAC-SHA256 hashes (originally plain text).

### 2. `orders`
Stores order records.
*   `Cust_PhoneNumber` acts as a Foreign Key linked to the `customers` table.
*   `Delivery_Status` is used by staff/admins to monitor fulfillment. Can be updated between `'Not Delivered'` and `'Delivered'`.

### 3. `categories`
Stores product categories.
*   Pre-populated with default categories: `Groceries (1)`, `Books (2)`, `Clothing (3)`, and `Stationery (4)`.

### 4. `products`
Stores inventory stock records.
*   `CategoryID` is a Foreign Key referencing `categories.CategoryID`.
*   Includes cascade deletion protections (cannot delete a category if products are still assigned to it).

### 5. `staff`
Stores employee records.
*   Includes default demo roles (e.g., `Akhil Tyagi` as CEO, `Priya Sharma` as Manager).
*   Password hashes are stored securely.

### 6. `attendance`
Stores log entries marking employee attendance logs.
*   `timestamp` is populated automatically on record creation.

---

## 🔄 Automated Setup & Seed Data
*   **Auto-Migration**: Upon application boot, the database connector queries the MySQL catalog for missing tables and builds them automatically.
*   **Seed Records**: If tables are empty, default records are seeded (including CEO and manager records, categories, and initial product entries).

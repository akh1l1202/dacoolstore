import mysql.connector

# Function 1: Establish a connection to the MySQL database
def connect_to_database():
    try:
        db = mysql.connector.connect(
            host='localhost',
            user='root',
            password='######',  #Replace the hashes with the paasword you setup for your local database server.
            database='dacoolstore',
        )
        return db

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Function to check if a table exists
def table_exists(cursor, table_name):
    cursor.execute("SHOW TABLES LIKE %s", (table_name,))
    return cursor.fetchone() is not None

# Function to check and create tables
def check_and_create_tables():
    connection = connect_to_database()
    if not connection:
        print("Database connection failed!")
        return

    cursor = connection.cursor()

    tables = {
        "attendance": """
            CREATE TABLE attendance (
                attendanceid INT AUTO_INCREMENT PRIMARY KEY,
                staffid INT DEFAULT NULL,
                staffname VARCHAR(255) DEFAULT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """,
        "categories": """
            CREATE TABLE categories (
                CategoryID INT PRIMARY KEY,
                CategoryName VARCHAR(255) NOT NULL
            );
        """,
        "customers": """
            CREATE TABLE customers (
                Cust_ID INT AUTO_INCREMENT PRIMARY KEY,
                Cust_Name VARCHAR(255),
                Cust_Gender TINYTEXT,
                Cust_EmailAddress VARCHAR(255),
                Cust_PhoneNumber VARCHAR(15) UNIQUE,
                Cust_Password VARCHAR(200)
            );
        """,
        "orders": """
            CREATE TABLE orders (
                OrderID INT AUTO_INCREMENT PRIMARY KEY,
                Cust_PhoneNumber VARCHAR(15),
                Cust_HomeAddress VARCHAR(500),
                Note VARCHAR(500),
                Time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                Delivery_Status VARCHAR(50) DEFAULT 'Not Delivered',
                FOREIGN KEY (Cust_PhoneNumber) REFERENCES customers(Cust_PhoneNumber)
            );
        """,
        "products": """
            CREATE TABLE products (
                ProductID INT AUTO_INCREMENT PRIMARY KEY,
                ProductName VARCHAR(255) NOT NULL,
                Price DECIMAL(10,2) NOT NULL,
                CategoryID INT,
                FOREIGN KEY (CategoryID) REFERENCES categories(CategoryID)
            );
        """,
        "staff": """
            CREATE TABLE staff (
                Staff_ID INT AUTO_INCREMENT PRIMARY KEY,
                Staff_Name VARCHAR(50) NOT NULL,
                Staff_Post CHAR(40),
                Gender ENUM('Male', 'Female', 'Other'),
                Password VARCHAR(255)
            );
        """
    }

    for table, create_query in tables.items():
        if table_exists(cursor, table):
            print(f"✅ Table '{table}' already exists.")
        else:
            cursor.execute(create_query)
            connection.commit()
            print(f"⚡ Table '{table}' was missing and has been created.")

    cursor.close()
    connection.close()

# Function 10: Insert customer data into the database
def insert_customer_data(db, name, gender, email, phone, password):
    try:
        cursor = db.cursor()
        insert_query = "INSERT INTO customers (Cust_Name, Cust_Gender, Cust_EmailAddress, Cust_PhoneNumber, Cust_Password) VALUES (%s, %s, %s, %s, %s);"
        values = (name, gender, email, phone, password)
        cursor.execute(insert_query, values)
        db.commit()
        cursor.close()
        return True

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False

# Function 14: Fetch product categories from the database
def fetch_categories(db):
    try:
        categories = []
        cursor = db.cursor()
        cursor.execute("SELECT DISTINCT CategoryName FROM categories;")
        for row in cursor.fetchall():
            categories.append(row[0])
        cursor.close()
        return categories
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []

# Function 15: Fetch products by category from the database
def fetch_products_by_category(db, category):
    try:
        products = []
        cursor = db.cursor()
        cursor.execute("SELECT ProductName FROM products WHERE CategoryID = (SELECT CategoryID FROM categories WHERE CategoryName = %s);", (category,))
        for row in cursor.fetchall():
            products.append(row[0])
        cursor.close()
        return products
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []

# Function 16: To fetch info of only the products in the list selected_product_names
def fetch_product_info_by_names(db, selected_product_names):
    try:
        cursor = db.cursor(dictionary=True)
        placeholders = ', '.join(['%s' for _ in selected_product_names])
        query = f"""
            SELECT c.CategoryName, p.ProductName, p.Price
            FROM products p
            JOIN categories c ON p.CategoryID = c.CategoryID
            WHERE p.ProductName IN ({placeholders});
        """
        cursor.execute(query, selected_product_names)
        product_info = cursor.fetchall()
        cursor.close()
        return product_info
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []

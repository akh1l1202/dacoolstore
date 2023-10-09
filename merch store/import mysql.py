import mysql.connector

# Assuming you have a list of selected product names
selected_products = ["Eggs", "Hoody", "Percy Jackson The Series"]

# Establish a database connection
db = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='akhil1202',
    database='test'
)

# Create a cursor
cursor = db.cursor(dictionary=True)

# Create a placeholder for the IN clause
placeholders = ', '.join(['%s'] * len(selected_products))

# Execute the query with the list of product names as a parameter
query = f"""
    SELECT p.ProductName, p.Price, c.CategoryName
    FROM products p
    JOIN categories c ON p.CategoryID = c.CategoryID
    WHERE p.ProductName IN ({placeholders})
"""

cursor.execute(query, selected_products)

# Fetch the results
results = cursor.fetchall()

# Iterate through the results
for row in results:
    print(row)

# Close cursor and database connection
cursor.close()
db.close()

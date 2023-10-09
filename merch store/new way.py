from functions import *
# Fetch all products and categories from the database
def fetch_all_products_and_categories(db):
    try:
        cursor = db.cursor(dictionary=True)

        # Join 'products' and 'categories' tables to get all product details
        cursor.execute("""
            SELECT p.ProductName, p.Price, c.CategoryName
            FROM products p
            JOIN categories c ON p.CategoryID = c.CategoryID;
        """)

        all_products = cursor.fetchall()

        cursor.close()
        return all_products
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []
fetch_all_products_and_categories(connect_to_database())
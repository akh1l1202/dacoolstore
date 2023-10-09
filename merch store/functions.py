import mysql.connector
import PySimpleGUI as sg

# Establish a connection to the MySQL database
def connect_to_database():
    try:
        db = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='akhil1202',
            database='test'
        )
        return db
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Insert customer data into the database
def insert_customer_data(db, name, gender, email, phone, password):
    try:
        cursor = db.cursor()

        # Insert customer information into the "customers" table
        insert_query = "INSERT INTO customers VALUES (%s, %s, %s, %s, %s);"
        values = (name, gender, email, phone, password)
        cursor.execute(insert_query, values)

        db.commit()
        cursor.close()
        return True
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False

# Fetch product categories from the database
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

# Fetch products by category from the database
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

# Create a new order in the database
def create_order(db, customer_id, category, selected_products):
    try:
        cursor = db.cursor()
        
        # Insert the order into the "orders" table (you need to create this table)
        # You should track customer_id, category, selected products, and total amount in the "orders" table
        
        db.commit()
        cursor.close()
        return True
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False

# Create a staff login window
def staff_login_window(db):
    layout = [
        [sg.Text("Enter your Staff ID"), sg.InputText(key='-STAFFID-')],
        [sg.Text("Enter your Password:"), sg.InputText(key='-PASSWORD-', password_char='*')],
        [sg.Button("Login"), sg.Button("Exit")],
    ]
    window = sg.Window("Staff Login", layout, finalize=True)

    cursor = db.cursor()

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Exit":
            break
        elif event == "Login":
            staffid = values['-STAFFID-']
            password = values['-PASSWORD-']

            # Query the database to verify the user's credentials using parameterized query
            cursor.execute("SELECT * FROM staff WHERE Staff_ID=%s AND Password=%s;", (staffid, password))
            user = cursor.fetchone()

            if user:
                sg.popup("Login Successful", f"Welcome, {user[1]}")
                window.close()
                # Open window which shows the staff person all the "Customers","Orders by customers" and "Option to add new categories and products"

            else:
                sg.popup_error("Login Failed", "Invalid username or password")

    db.close()
    window.close()


# Create a customer registration window
def customer_registration_window():
    sg.theme('DarkBlue')

    layout = [
        [sg.Text("Enter full name:"), sg.Input(key="-NAME-", size=(30, 1))],
        [sg.Text("Select gender:"), sg.Radio("Male", "GENDER", key="-MALE-", default=True), sg.Radio("Female", "GENDER", key="-FEMALE-")],
        [sg.Text("Enter your email address:"), sg.Input(key="-EMAIL-", size=(30, 1))],
        [sg.Text("Enter your phone number:"), sg.Input(key="-PHONE-", size=(30, 1))],
        [sg.Text("Enter your password"), sg.Input(key="-PASS-", password_char='*', size=(30, 1))],
        [sg.Button("Register"), sg.Button("Exit")]
    ]

    window = sg.Window('Customer Registration', layout)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == "Exit":
            break
        elif event == "Register":
            name = values["-NAME-"]
            gender = "Male" if values["-MALE-"] else "Female"
            email = values["-EMAIL-"]
            phone = values["-PHONE-"]
            password = values["-PASS-"]

            db = connect_to_database()

            if db:
                if insert_customer_data(db, name, gender, email, phone, password):
                    sg.popup("Customer Registration Successful!")
                    window.close()

                    # Open the customer order window
                    customer_order_window(db)

                else:
                    sg.popup_error("Error occurred during registration. Please try again later.")

                db.close()

    window.close()

# Create a login window for customers
def customer_login_window(db):
    layout = [
        [sg.Text("Phone Number:"), sg.InputText(key='-PHONE-')],
        [sg.Text("Password:"), sg.InputText(key='-PASSWORD-', password_char='*')],
        [sg.Button("Login"), sg.Button("Exit")],
    ]
    window = sg.Window("Customer Login", layout, finalize=True)
    
    cursor = db.cursor()

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == "Exit":
            break
        elif event == "Login":
            phone = values['-PHONE-']
            password = values['-PASSWORD-']

            # Query the database to verify the user's credentials using parameterized query
            cursor.execute("SELECT * FROM customers WHERE Cust_PhoneNumber=%s AND Cust_Password=%s;", (phone, password))
            user = cursor.fetchone()

            if user:
                sg.popup("Login Successful", f"Welcome, {user[0]}")
                window.close()
                # Open customer order window
                customer_order_window(db)

            else:
                sg.popup_error("Login Failed", "Invalid username or password")

    db.close()
    window.close()

# Create a customer order window
def customer_order_window(db):
    sg.theme('DarkBlue')

    layout = [
        [sg.Text("Customer Options")],
        [sg.Button("Create New Order"), sg.Button("See Existing Orders"), sg.Exit()]
    ]

    window = sg.Window('Customer Options', layout)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == "Exit":
            break
        elif event == "Create New Order":
            window.close()
            # Open the order creation window
            create_order_window(db)
        elif event == "See Existing Orders":
            sg.popup("Seeing Existing Orders...")  # Add logic to view existing orders here

    window.close()

# Create a window for order creation
def create_order_window(db):
    sg.theme('DarkBlue')

    categories = fetch_categories(db)

    layout = [
        [sg.Text("Select Product Categories:")],
        [sg.Listbox(categories, key="-CATEGORIES-", select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, size=(40, 6), enable_events=True)],
        [sg.Text("Select Products:")],
        [sg.Listbox(values=[], key="-PRODUCTS-", select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, size=(40, 6))],
        [sg.Button("Confirm Selection"), sg.Exit()],
        [sg.Text("Selected Products:")],
        [sg.Listbox(values=[], key="-SELECTED-PRODUCTS-", size=(40, 6))],  # Display selected products
    ]

    window = sg.Window("Create New Order", layout)
    selected_product_names = []  # Store selected product names

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == "Exit":
            break
        elif event == "-CATEGORIES-":
            selected_categories = values["-CATEGORIES-"]
            selected_products = []

            for category in selected_categories:
                selected_products.extend(fetch_products_by_category(db, category))

            window["-PRODUCTS-"].update(values=selected_products)
        elif event == "Confirm Selection":
            selected_category = values["-CATEGORIES-"]
            selected_products = values["-PRODUCTS-"]

            if selected_products and selected_category:
                selected_product_names.extend(selected_products)
                window["-SELECTED-PRODUCTS-"].update(values=selected_product_names)  # Update the selected products list
                
                billing_window(db,selected_products)

                window.close()
                break

    window.close()



# Function to fetch order details of the selected products from the database
def fetch_order_details(db,selected_products):
    try:
        cursor = db.cursor(dictionary=True)

        # Join 'products' and 'categories' tables to get order details
        cursor.execute("""
            SELECT p.ProductName, p.Price, c.CategoryName
            FROM products p
            JOIN categories c ON p.CategoryID = c.CategoryID
            WHERE p.ProductName IN (%s);
        """, (", ".join(selected_products),))

        order_details = cursor.fetchall()

        cursor.close()
        return order_details
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []

 # Function to display the billing window
def billing_window(db, selected_products):
    sg.theme('DarkBlue')
    order_details = fetch_order_details(db, selected_products)


    # Define the layout of the billing window
    layout = [
        [sg.Text("Billing Details", font=("Helvetica", 18))],
        [sg.Table(values=[], headings=["Sr. No.", "Category Name", "Product Name", "Product Price"], auto_size_columns=False,
                  col_widths=[5, 20, 20, 15], justification="right", num_rows=10, key='-TABLE-')],
        [sg.Text("Total Amount:", font=("Helvetica", 14)), sg.Text("", size=(10, 1), font=("Helvetica", 14), key='-TOTAL-')],
        [sg.Button("Confirm Order"), sg.Exit()]
    ]

    window = sg.Window('Billing Window', layout, finalize=True)

    # Initialize variables for serial numbers and total amount
    serial_number = 1
    total_amount = 0.0

    # Populate the table with order details
    table_data = []
    for order in order_details:
        category_name = order["CategoryName"]
        product_name = order["ProductName"]
        product_price = order["ProductPrice"]
        total_amount += product_price

        table_data.append([serial_number, category_name, product_name, f"Rs.{product_price:.2f}"])
        serial_number += 1

    window['-TABLE-'].update(values=table_data)
    window['-TOTAL-'].update(f"${total_amount:.2f}")

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == "Exit":
            break
        elif event == "Confirm Order":
            sg.popup("Order Confirmed!")
            window.close()
            break


    window.close()


# Main function
def main():
    sg.theme('DarkBlue')

    # Create a window for user type selection
    layout_choice = [
        [sg.Text("Are you a staff member or a customer?")],
        [sg.Button("Staff"), sg.Button("New User"), sg.Button("Existing User"), sg.Exit()]
    ]

    window_choice = sg.Window('User Type', layout_choice)

    while True:
        event_choice, _ = window_choice.read()

        if event_choice == sg.WIN_CLOSED or event_choice == "Exit":
            break
        elif event_choice == "Staff":
            sg.popup_ok("You selected 'Staff'.")
        elif event_choice == "New User":
            window_choice.close()  # Close the current window
            customer_registration_window()
        elif event_choice == "Existing User":
            window_choice.close()  # Close the current window
            customer_login_window(connect_to_database())

    window_choice.close()


if __name__ == "__main__":
    main()
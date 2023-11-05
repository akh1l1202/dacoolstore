import mysql.connector
import PySimpleGUI as sg

# Function 1: Establish a connection to the MySQL database
def connect_to_database():
    try:
        db = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='akhil1202',
            database='dacoolstore'
        )
        return db
    except mysql.connector.Error as error:
        print(f"Error: {error}")
        return None

# Function 2: Create a login window for staff
def staff_login_window(db):
    layout = [
        [sg.Text("Staff ID:"), sg.InputText(key='-ID-')],
        [sg.Text("Password:"), sg.InputText(key='-PASSWORD-', password_char='*')],
        [sg.Button("Login"), sg.Button("Exit")],
    ]
    window = sg.Window("Staff Login", layout, finalize=True)
    
    cursor = db.cursor()

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == "Exit":
            break
        elif event == "Login":
            cid = values['-ID-']
            password = values['-PASSWORD-']

            # Query the database to verify the user's credentials using parameterized query
            cursor.execute("SELECT * FROM staff WHERE Staff_ID=%s AND Password=%s;", (cid, password))
            user = cursor.fetchone()

            if user:
                window.hide()
                sg.popup("Login Successful", f"Welcome, {user[1]}")
                window.close()
                # Open window which has buttons "see existing orders", "see all customer details", "add a new product", "add new category"
                staff_options_window()

            else:
                sg.popup_error("Login Failed", "Invalid username or password")

    db.close()
    window.close()

# Function 3: Once the staff logins asking them what they want to do
def staff_options_window():
    sg.theme('BrownBlue')

    layout = [
        [sg.Text("Staff Options", font=("Helvetica", 18))],
        [sg.Button("View Customer Orders")],
        [sg.Button("Customer Details")],
        [sg.Button("Add Product")],
        [sg.Button("Add Category")],
        [sg.Button("Exit")]
    ]

    window = sg.Window("Staff Options", layout, finalize=True)

    while True:
        event, _ = window.read()

        if event in ('View Customer Orders','Customer Details','Add Product','Add Category'):
            window.close()
        if event == sg.WIN_CLOSED or event == "Exit":
            break
        elif event == "View Customer Orders":
            display_all_orders(connect_to_database())
        elif event == "Customer Details":
            fetch_all_and_displaywindow(connect_to_database())
        elif event == "Add Product":
            # Call a function to add a new product
            add_product_to_db(connect_to_database())
        elif event == "Add Category":
            # Call a function to add a new category
            add_category_to_db(connect_to_database())

    window.close()

# Function 4: To display all the orders
def display_all_orders(db):
    sg.theme('BrownBlue')

    layout = [
        [sg.Text("All Orders", font=("Helvetica", 18))],
        [sg.Table(values=[], headings=["Customer ID", "Name", "Phone Number", "Address", "Note", "Time"], 
                  auto_size_columns=False, col_widths=[9, 20, 15, 25, 25, 15], display_row_numbers=False, 
                  justification="center", num_rows=20, key='-TABLE-')],
        [sg.Button("Exit"), sg.Button('Back')]
    ]

    window = sg.Window("All Orders", layout, finalize=True)

    try:
        cursor = db.cursor(dictionary=True)

        # Fetch all orders from the table
        cursor.execute("SELECT * FROM orders JOIN customers ON orders.Cust_PhoneNumber = customers.Cust_PhoneNumber;")
        orders = cursor.fetchall()

        # Update the table with order details
        table_data = []
        for order in orders:
            table_data.append([order["Cust_ID"], order["Cust_Name"], order["Cust_PhoneNumber"], order["Cust_HomeAddress"], order["Note"], order["Time"]])

        window['-TABLE-'].update(values=table_data)

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == "Exit":
            break
        if event == 'Back':
            window.close()
            staff_options_window()


    window.close()

# Function 5: To fetch all from the table customers and display it in a window see_customer_data
def fetch_all_and_displaywindow(db):
    try:
        cursor = db.cursor()
        cursor.execute("SELECT * from customers")
        customer_data = cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error: {err}")

    sg.theme('BrownBlue')

    layout = [
        [sg.Text("Customer Details", font=("Helvetica", 18))],
        [sg.Table(values=customer_data, headings=["Name", "Gender", "Email", "Phone", "Password"], auto_size_columns=False,
                  display_row_numbers=False, justification="center", num_rows=10, key='-TABLE-')],
        [sg.Button("Exit")]
    ]

    window = sg.Window("Customer Details", layout, finalize=True)

    while True:
        event, _ = window.read()

        if event == sg.WIN_CLOSED or event == "Exit":
            break

    window.close()

# Function 6: To take inputs from the staff for the new product and then insert the values into the products table
def add_product_to_db(db):
    sg.theme('BrownBlue')

    layout = [
        [sg.Text("Add New Product", font=("Helvetica", 18))],
        [sg.Text("Product Name:"), sg.InputText(key='-PRODUCTNAME-')],
        [sg.Text("Price:"), sg.InputText(key='-PRICE-')],
        [sg.Text("Category ID:"), sg.InputText(key='-CATEGORYID-')],
        [sg.Button("Add Product"), sg.Button("Exit")]
    ]

    window = sg.Window("Add Product", layout, finalize=True)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == "Exit":
            break
        elif event == "Add Product":
            window.close()
            product_name = values['-PRODUCTNAME-']
            price = values['-PRICE-']
            category_id = values['-CATEGORYID-']

            try:
                cursor = db.cursor()

                insert_query = "INSERT INTO products (ProductName, Price, CategoryID) VALUES (%s, %s, %s);"
                values = (product_name, price, category_id)
                cursor.execute(insert_query, values)

                db.commit()
                sg.popup("Product Added Successfully!")
            except mysql.connector.Error as err:
                sg.popup_error(f"Error occurred during product addition: {err}")

    window.close()

# Function 7: To take inputs from the staff for the new category and then insert the values into the table categories
def add_category_to_db(db):
    sg.theme('BrownBlue')

    layout = [
        [sg.Text("Add New Category", font=("Helvetica", 18))],
        [sg.Text("Category ID:"), sg.InputText(key='-CATEGORYID-')],
        [sg.Text("Category Name:"), sg.InputText(key='-CATEGORYNAME-')],
        [sg.Button("Add Category"), sg.Button("Exit")]
    ]

    window = sg.Window("Add Category", layout, finalize=True)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == "Exit":
            break
        elif event == "Add Category":
            window.hide()
            category_id = values['-CATEGORYID-']
            category_name = values['-CATEGORYNAME-']

            try:
                cursor = db.cursor()

                insert_query = "INSERT INTO categories (CategoryID, CategoryName) VALUES (%s, %s);"
                values = (category_id, category_name)
                cursor.execute(insert_query, values)

                db.commit()
                sg.popup("Category Added Successfully!")
            except mysql.connector.Error as err:
                sg.popup_error(f"Error occurred during category addition: {err}")

    window.close()

# Function 8: Create a customer registration window
def customer_registration_window():
    sg.theme('BrownBlue')

    layout = [
        [sg.Text("Enter full name:"), sg.Input(key="-NAME-", size=(30, 1))],
        [sg.Text("Select gender:"), sg.Radio("Male", "GENDER", key="-MALE-", default=True), sg.Radio("Female", "GENDER", key="-FEMALE-")],
        [sg.Text("Enter your email address:"), sg.Input(key="-EMAIL-", size=(30, 1))],
        [sg.Text("Enter your phone number:"), sg.Input(key="-PHONE-", size=(30, 1))],
        [sg.Text("Enter your password"), sg.Input(key="-PASS-", password_char='*', size=(30, 1))],
        [sg.Button("Register"), sg.Button("Exit")]
    ]

    window = sg.Window('Customer Registration', layout)
    customer_phone = None

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == "Exit":
            break
        elif event == "Register":

            window.close()
            name = values["-NAME-"]
            gender = "Male" if values["-MALE-"] else "Female"
            email = values["-EMAIL-"]
            phone = values["-PHONE-"]
            password = values["-PASS-"]

            db = connect_to_database()

            if db:
                if insert_customer_data(db, name, gender, email, phone, password):
                    sg.popup("Customer Registration Successful!")
                    customer_phone = phone
                    window.close()

                    # Open the customer order window
                    customer_order_window(db)

                else:
                    sg.popup_error("Error occurred during registration. Please try again later.")

                db.close()

# Function 9: Insert customer data into the database
def insert_customer_data(db, name, gender, email, phone, password):
    try:
        cursor = db.cursor()

        # Insert customer information into the "customers" table
        insert_query = "INSERT INTO customers (Cust_Name, Cust_Gender, Cust_EmailAddress, Cust_PhoneNumber, Cust_Password) VALUES (%s, %s, %s, %s, %s);"
        values = (name, gender, email, phone, password)
        cursor.execute(insert_query, values)

        db.commit()
        cursor.close()
        return True
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False

# Function 10: Create a login window for customers
def customer_login_window(db):
    sg.theme('BrownBlue')
    layout = [
        [sg.Text("Phone Number:"), sg.InputText(key='-PHONE-')],
        [sg.Text("Password:"), sg.InputText(key='-PASSWORD-', password_char='*')],
        [sg.Button("Login"), sg.Button("Exit")],
    ]
    window = sg.Window("Customer Login", layout, finalize=True)
    
    cursor = db.cursor()
    customer_phone = None

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
                sg.popup("Login Successful", f"Welcome, {user[1]}")
                customer_phone = phone
                window.close()
                # Open customer order window
                customer_order_window(db)

            else:
                sg.popup_error("Login Failed", "Invalid username or password")

    db.close()
    window.close()

# Function 11: Create a customer order window
def customer_order_window(db):
    sg.theme('BrownBlue')

    layout = [
        [sg.Text("Select what you want to do:")],
        [sg.Button("Create New Order"), sg.Button("See Existing Orders"), sg.Exit()]
    ]

    window = sg.Window('Customer Options', layout)

    while True:
        event, values = window.read()
        if event in ('See Existing Orders','Create New Order'):
            window.close()
        if event == sg.WIN_CLOSED or event == "Exit":
            break
        elif event == "Create New Order":
            window.close()
            # Open the order creation window
            create_order_window(db)
        elif event == "See Existing Orders":
            display_customer_orders(db)

    window.close()

# Function 12: Create a window for order creation
def create_order_window(db):
    sg.theme('BrownBlue')

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
            window.hide()
            selected_category = values["-CATEGORIES-"]
            selected_products = values["-PRODUCTS-"]

            if selected_products and selected_category:
                selected_product_names.extend(selected_products)
                window["-SELECTED-PRODUCTS-"].update(values=selected_product_names)  # Update the selected products list

                # Call the billing window function to display billing details
                product_info = fetch_product_info_by_names(db, selected_product_names)
                billing_window = display_billing_window(product_info)

                # Allow the billing window to stay open until the user closes it
                while True:
                    event, _ = billing_window.read()

                    if event == sg.WIN_CLOSED or event == "Exit":
                        break

                window.close()
                break

    window.close()

# Function 13: Fetch product categories from the database
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

# Function 14: Fetch products by category from the database
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

# Function 15: To fetch info of only the products in the list selected_product_names
def fetch_product_info_by_names(db, selected_product_names):
    try:
        cursor = db.cursor(dictionary=True)

        # Create placeholders for the list of product names
        placeholders = ', '.join(['%s' for _ in selected_product_names])

        # Construct the SQL query with placeholders
        query = f"""
            SELECT c.CategoryName, p.ProductName, p.Price
            FROM products p
            JOIN categories c ON p.CategoryID = c.CategoryID
            WHERE p.ProductName IN ({placeholders});
        """
        
        print("Query:", query)  # Print the query for debugging
        cursor.execute(query, selected_product_names)

        product_info = cursor.fetchall()

        cursor.close()
        return product_info
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []

# Function 16: To create the billing window
def display_billing_window(product_details):
    sg.theme('BrownBlue')

    # Define the layout of the billing window
    layout = [
    [sg.Text("Billing Details", font=("Helvetica", 18))],
    [sg.Table(values=[], headings=["Sr. No.", "Category Name", "Product Name", "Product Price"], auto_size_columns=False,
              col_widths=[5, 20, 20, 15], justification="center", num_rows=10, key='-TABLE-')],
    [sg.Text("Total Amount:", font=("Helvetica", 14)), sg.Text("", size=(10, 1), font=("Helvetica", 14), key='-TOTAL-', justification="center")],
    [sg.Button("Confirm Order"), sg.Exit()]
]

    window = sg.Window('Billing Window', layout, finalize=True)

    # Initialize variables for serial numbers and total amount
    serial_number = 1
    total_amount = 0.0

    # Populate the table with order details
    table_data = []
    for order in product_details:
        category_name = order["CategoryName"]
        product_name = order["ProductName"]
        product_price = float(order["Price"])
        total_amount += product_price

        table_data.append([serial_number, category_name, product_name, f"Rs.{product_price:.2f}"])
        serial_number += 1

    window['-TABLE-'].update(values=table_data)
    window['-TOTAL-'].update(f"Rs.{total_amount:.2f}")
    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == "Exit":
            break
        elif event == "Confirm Order":
            window.hide()
            get_customer_details_and_put_it_in_orders(connect_to_database())
            window.close()
            
    return window

# Function 17: To take inputs from the user about their order and inserts it into table orders
def get_customer_details_and_put_it_in_orders(db):
    sg.theme('BrownBlue')

    layout = [
        [sg.Text("Enter your contact details:")],
        [sg.Text("Billing Phone Number:"), sg.InputText(key="-PHONE-")],
        [sg.Text("Address:"), sg.InputText(key="-ADDRESS-")],
        [sg.Text("Extra Notes:"), sg.InputText(key="-EXTRA-NOTES-")],
        [sg.Button("Confirm"), sg.Button("Cancel")]
    ]

    window = sg.Window("Customer Details", layout, finalize=True)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == "Cancel":
            break
        elif event == "Confirm":
            phone_number = values["-PHONE-"]
            address = values["-ADDRESS-"]
            extra_notes = values["-EXTRA-NOTES-"]

            try:
                cursor = db.cursor()
                insert_query = "INSERT INTO orders (Cust_PhoneNumber, Cust_HomeAddress, Note) VALUES (%s, %s, %s);"
                values = (phone_number, address, extra_notes)
                cursor.execute(insert_query, values)
                db.commit()
                cursor.close()
                sg.popup("Details saved successfully!")
            except mysql.connector.Error as err:
                print(f"Error: {err}")
            # You can handle the data as needed, such as saving it to the database
            # or performing any other required actions.

            
            window.close()
            break

    window.close()

# Function 18: To display the customers order info if they select see existing orders, in a window ask for their phone number and then retrieve data from database
def display_customer_orders(db):
    sg.theme('BrownBlue')

    # Create a layout for the window
    layout = [
        [sg.Text("Enter Billing Phone Number:"), sg.InputText(key='-PHONE-')],
        [sg.Button("Show Orders"), sg.Button("Exit")],
        [sg.Table(values=[], headings=["Order ID", "Address", "Notes", "Order Time"], auto_size_columns=False,
                  col_widths=[10, 30, 40, 15], display_row_numbers=False, justification="right", key='-TABLE-', row_height=35)]
    ]

    window = sg.Window("Your Existing Orders", layout, finalize=True)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == "Exit":
            break
        elif event == "Show Orders":
            phone_number = values["-PHONE-"]

            if phone_number:
                try:
                    cursor = db.cursor(dictionary=True)

                    # Fetch orders for the given phone number
                    cursor.execute("SELECT * FROM orders WHERE Cust_PhoneNumber = %s;", (phone_number,))
                    orders = cursor.fetchall()

                    if orders:
                        # Update the table with the order details
                        table_data = []
                        for order in orders:
                            table_data.append([order["OrderID"], order["Cust_HomeAddress"], order["Note"], order["Time"]])

                        window['-TABLE-'].update(values=table_data)
                    else:
                        sg.popup("No orders found for the given phone number.")
                except mysql.connector.Error as err:
                    print(f"Error: {err}")
            else:
                sg.popup("Please enter a valid phone number.")

    window.close()

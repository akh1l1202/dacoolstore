import PySimpleGUI as sg
from database import connect_to_database, insert_customer_data, fetch_categories, fetch_products_by_category, fetch_product_info_by_names
from utils import main
import mysql.connector

def customer_registration_window():
    sg.theme('BrownBlue')
    layout = [
        [sg.Text("Enter full name:"), sg.Input(key="-NAME-", size=(30, 1))],
        [sg.Text("Select gender:"), sg.Radio("Male", "GENDER", key="-MALE-", default=True), sg.Radio("Female", "GENDER", key="-FEMALE-")],
        [sg.Text("Enter your email address:"), sg.Input(key="-EMAIL-", size=(30, 1))],
        [sg.Text("Enter your phone number:"), sg.Input(key="-PHONE-", size=(30, 1))],
        [sg.Text("Enter your password"), sg.Input(key="-PASS-", password_char='*', size=(30, 1))],
        [sg.Button("Register", bind_return_key=True), sg.Exit(), sg.Button('Back')]
    ]

    window = sg.Window('Customer Registration', layout)
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

            if db and insert_customer_data(db, name, gender, email, phone, password):
                sg.popup(f"Welcome {name}! Your account has been successfully created.")
                window.close()
                from utils import main
                main()
            else:
                sg.popup_error("Error occurred during registration. Please try again later.")

            db.close()
        elif event == 'Back':
            window.hide()
            from utils import main
            main()
        window.close()

def customer_login_window(db):

    sg.theme('BrownBlue')
    layout = [
        [sg.Text("Phone Number:"), sg.InputText(key='-PHONE-')],
        [sg.Text("Password:"), sg.InputText(key='-PASSWORD-', password_char='*')],
        [sg.Button("Login", bind_return_key=True), sg.Exit(), sg.Button('Back')],
    ]
    window = sg.Window("Customer Login", layout, finalize=True)
    cursor = db.cursor()

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == "Exit":
            break
        elif event == "Login":
            window.hide()
            phone = values['-PHONE-']
            password = values['-PASSWORD-']

            # Query the database to verify the user's credentials using parameterized query
            cursor.execute("SELECT * FROM customers WHERE Cust_PhoneNumber=%s AND Cust_Password=%s;", (phone, password))
            user = cursor.fetchone()

            if user:
                sg.popup("Login Successful", f"Welcome, {user[1]}. Have a lovely day :D \n\n")
                
                window.close()
                # Open customer order window
                customer_order_window(db)

            else:
                sg.popup_error("Login Failed", "Invalid username or password")

        elif event == 'Back':
            window.hide()
            main()

    db.close()
    window.close()

def customer_order_window(db):
    sg.theme('BrownBlue')

    layout = [
        [sg.Text("Select what you want to do:")],
        [sg.Button("Create New Order"), sg.Button("See Existing Orders"), sg.Exit(), sg.Button('Logout')]
    ]

    window = sg.Window('Customer Options', layout)

    while True:
        event, values = window.read()
        if event in ('See Existing Orders','Create New Order','Logout'):
            window.hide()
        if event == sg.WIN_CLOSED or event == "Exit":
            break
        elif event == "Create New Order":
            window.close()
            create_order_window(db)
        elif event == "See Existing Orders":
            display_customer_orders(db)
        elif event == 'Logout':
            customer_login_window(db)

    window.close()

def create_order_window(db):
    sg.theme('BrownBlue')

    categories = fetch_categories(db)

    layout = [
        [sg.Text("Select Product Categories:")],
        [sg.Listbox(categories, key="-CATEGORIES-", select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, size=(40, 6), enable_events=True)],
        [sg.Text("Select Products:")],
        [sg.Listbox(values=[], key="-PRODUCTS-", select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, size=(40, 6))],
        [sg.Button("Confirm Selection", bind_return_key=True), sg.Exit(), sg.Button('Back')],
        [sg.Text("Selected Products:")],
        [sg.Listbox(values=[], key="-SELECTED-PRODUCTS-", size=(40, 6))],  # Display selected products
    ]

    window = sg.Window("Create New Order", layout)
    selected_product_names = []  # Store selected product names

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, "Exit",):
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
        if event == 'Back':
            window.close()
            customer_order_window(db)

    window.close()

def display_customer_orders(db):
    sg.theme('BrownBlue')

    # Create a layout for the window
    layout = [
        [sg.Text("Enter Billing Phone Number:"), sg.InputText(key='-PHONE-')],
        [sg.Button("Show Orders"), sg.Exit(), sg.Button('Back')],
        [sg.Table(values=[], headings=["Order ID", "Address", "Notes", "Order Time", "Status"], auto_size_columns=False,
                  col_widths=[10, 25, 20, 15, 13], display_row_numbers=False, justification="center ", key='-TABLE-', row_height=35)]
    ]

    window = sg.Window("Your Existing Orders", layout, finalize=True,)

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
                            table_data.append([order["OrderID"], order["Cust_HomeAddress"], order["Note"], order["Time"], order["Delivery_Status"]])

                        window['-TABLE-'].update(values=table_data)
                    else:
                        sg.popup("No orders found for the given phone number.")
                except mysql.connector.Error as err:
                    print(f"Error: {err}")
            else:
                sg.popup("Please enter a valid phone number.")

        elif event == 'Back':
            window.hide()
            customer_order_window(db)

    window.close()

def get_customer_details_and_put_it_in_orders(db):
    sg.theme('BrownBlue')

    layout = [
        [sg.Text("Enter your contact details:")],
        [sg.Text("Billing Phone Number:"), sg.InputText(key="-PHONE-")],
        [sg.Text("Address:"), sg.InputText(key="-ADDRESS-")],
        [sg.Text("Extra Notes:"), sg.InputText(key="-EXTRA-NOTES-")],
        [sg.Button("Confirm", bind_return_key=True), sg.Button("Cancel")]
    ]

    window = sg.Window("Customer Details", layout, finalize=True)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break
        elif event == "Confirm":
            window.hide()
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
                sg.popup(f"Order successfully created! \nWill be delivered at {address}.\n\n")
                customer_order_window(db)
            except mysql.connector.Error as err:
                print(f"Error: {err}")

        elif event == 'Cancel':
            window.hide()
            customer_order_window(db)
            
            window.close()
            break

    window.close()

def display_billing_window(product_details):
    sg.theme('BrownBlue')

    # Define the layout of the billing window
    layout = [
    [sg.Text("Billing Details", font=("Helvetica", 18))],
    [sg.Table(values=[], headings=["Sr. No.", "Product Name", "Category Name", "Product Price"], auto_size_columns=False,
              col_widths=[5, 20, 20, 15], justification="center", num_rows=10, key='-TABLE-')],
    [sg.Text("Total Amount:", font=("Helvetica", 14)), sg.Text("", size=(10, 1), font=("Helvetica", 14), key='-TOTAL-', justification="center")],
    [sg.Text("(Your order can not be edited once you select Confirm Order)")],
    [sg.Button("Confirm Order", bind_return_key=True), sg.Exit(), sg.Button('Change your Order')]
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

        table_data.append([serial_number, product_name, category_name, f"Rs.{product_price:.2f}"])
        serial_number += 1

    window['-TABLE-'].update(values=table_data)
    window['-TOTAL-'].update(f"Rs.{total_amount:.2f}")
    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, "Exit"):
            break
        elif event == "Confirm Order":
            window.hide()
            get_customer_details_and_put_it_in_orders(connect_to_database())
            window.close()
        elif event == 'Change your Order':
            window.hide()
            create_order_window(connect_to_database())
            
    window.close()
    return window
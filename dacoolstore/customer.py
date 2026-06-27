import mysql.connector
import PySimpleGUI as sg

from dacoolstore.database import (
    fetch_categories,
    fetch_product_info_by_names,
    fetch_products_by_category,
    insert_customer_data,
)
from dacoolstore.security import verify_password


def customer_registration_window(db) -> str:
    """Window for new customer registration."""
    sg.theme("BrownBlue")
    layout = [
        [sg.Text("Enter full name:"), sg.Input(key="-NAME-", size=(30, 1))],
        [
            sg.Text("Select gender:"),
            sg.Radio("Male", "GENDER", key="-MALE-", default=True),
            sg.Radio("Female", "GENDER", key="-FEMALE-"),
        ],
        [sg.Text("Enter your email address:"), sg.Input(key="-EMAIL-", size=(30, 1))],
        [sg.Text("Enter your phone number:"), sg.Input(key="-PHONE-", size=(30, 1))],
        [sg.Text("Enter your password:"), sg.Input(key="-PASS-", password_char="*", size=(30, 1))],
        [sg.Button("Register", bind_return_key=True), sg.Exit(), sg.Button("Back")],
    ]

    window = sg.Window("Customer Registration", layout)
    exit_status = "BACK"
    try:
        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, "Exit"):
                exit_status = "EXIT"
                break
            elif event == "Back":
                break
            elif event == "Register":
                name = values["-NAME-"].strip()
                gender = "Male" if values["-MALE-"] else "Female"
                email = values["-EMAIL-"].strip()
                phone = values["-PHONE-"].strip()
                password = values["-PASS-"]

                # Input Validations
                if not name or not email or not phone or not password:
                    sg.popup_error("Validation Error", "All fields are required!")
                    continue

                if "@" not in email or "." not in email:
                    sg.popup_error("Validation Error", "Please enter a valid email address.")
                    continue

                if not phone.isdigit() or len(phone) < 8:
                    sg.popup_error(
                        "Validation Error", "Please enter a valid phone number (digits only, at least 8 digits)."
                    )
                    continue

                if insert_customer_data(db, name, gender, email, phone, password):
                    sg.popup(f"Welcome {name}! Your account has been successfully created.")
                    break
                else:
                    sg.popup_error(
                        "Registration Failed",
                        "Error occurred during registration. The phone number might already exist.",
                    )
    finally:
        window.close()
    return exit_status


def customer_login_window(db) -> str:
    """Window for customer login."""
    sg.theme("BrownBlue")
    layout = [
        [sg.Text("Phone Number:"), sg.InputText(key="-PHONE-")],
        [sg.Text("Password:"), sg.InputText(key="-PASSWORD-", password_char="*")],
        [sg.Button("Login", bind_return_key=True), sg.Exit(), sg.Button("Back")],
    ]
    window = sg.Window("Customer Login", layout, finalize=True)
    exit_status = "BACK"

    try:
        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, "Exit"):
                exit_status = "EXIT"
                break
            elif event == "Back":
                break
            elif event == "Login":
                phone = values["-PHONE-"].strip()
                password = values["-PASSWORD-"]

                if not phone or not password:
                    sg.popup_error("Login Failed", "Please enter both phone number and password.")
                    continue

                cursor = None
                try:
                    cursor = db.cursor()
                    cursor.execute(
                        "SELECT Cust_ID, Cust_Name, Cust_Gender, Cust_EmailAddress, Cust_PhoneNumber, Cust_Password FROM customers WHERE Cust_PhoneNumber=%s;",
                        (phone,),
                    )
                    user = cursor.fetchone()

                    if user and verify_password(password, user[5]):
                        sg.popup("Login Successful", f"Welcome, {user[1]}. Have a lovely day :D")
                        window.hide()
                        sub_status = customer_order_window(db)
                        if sub_status == "EXIT":
                            exit_status = "EXIT"
                            break
                        # When returning from order window, unhide login
                        window.unhide()
                    else:
                        sg.popup_error("Login Failed", "Invalid phone number or password")
                except mysql.connector.Error as err:
                    sg.popup_error("Database Error", f"Error querying user: {err}")
                finally:
                    if cursor:
                        cursor.close()
    finally:
        window.close()
    return exit_status


def customer_order_window(db) -> str:
    """Customer options dashboard window."""
    sg.theme("BrownBlue")
    layout = [
        [sg.Text("Select what you want to do:")],
        [sg.Button("Create New Order"), sg.Button("See Existing Orders"), sg.Exit(), sg.Button("Logout")],
    ]
    window = sg.Window("Customer Options", layout)
    exit_status = "LOGOUT"

    try:
        while True:
            event, _ = window.read()
            if event in (sg.WIN_CLOSED, "Exit"):
                exit_status = "EXIT"
                break
            elif event == "Logout":
                break
            elif event == "Create New Order":
                window.hide()
                sub_status = create_order_window(db)
                if sub_status == "EXIT":
                    exit_status = "EXIT"
                    break
                window.unhide()
            elif event == "See Existing Orders":
                window.hide()
                sub_status = display_customer_orders(db)
                if sub_status == "EXIT":
                    exit_status = "EXIT"
                    break
                window.unhide()
    finally:
        window.close()
    return exit_status


def create_order_window(db) -> str:
    """Order placement and category selection window."""
    sg.theme("BrownBlue")
    categories = fetch_categories(db)

    layout = [
        [sg.Text("Select Product Categories:")],
        [
            sg.Listbox(
                categories,
                key="-CATEGORIES-",
                select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
                size=(40, 6),
                enable_events=True,
            )
        ],
        [sg.Text("Select Products:")],
        [sg.Listbox(values=[], key="-PRODUCTS-", select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, size=(40, 6))],
        [sg.Button("Confirm Selection", bind_return_key=True), sg.Exit(), sg.Button("Back")],
        [sg.Text("Selected Products:")],
        [sg.Listbox(values=[], key="-SELECTED-PRODUCTS-", size=(40, 6))],
    ]

    window = sg.Window("Create New Order", layout)
    selected_product_names = []
    exit_status = "BACK"

    try:
        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, "Exit"):
                exit_status = "EXIT"
                break
            elif event == "Back":
                break
            elif event == "-CATEGORIES-":
                selected_categories = values["-CATEGORIES-"]
                selected_products = []
                for category in selected_categories:
                    selected_products.extend(fetch_products_by_category(db, category))
                window["-PRODUCTS-"].update(values=selected_products)
            elif event == "Confirm Selection":
                selected_products = values["-PRODUCTS-"]
                if selected_products:
                    selected_product_names = list(selected_products)
                    window["-SELECTED-PRODUCTS-"].update(values=selected_product_names)

                    product_info = fetch_product_info_by_names(db, selected_product_names)

                    window.hide()
                    billing_status = display_billing_window(db, product_info)
                    if billing_status == "EXIT":
                        exit_status = "EXIT"
                        break
                    elif billing_status == "CONFIRMED":
                        exit_status = "CONFIRMED"
                        break
                    else:
                        window.unhide()
                else:
                    sg.popup_error("Selection Error", "Please select at least one product.")
    finally:
        window.close()
    return exit_status


def display_customer_orders(db) -> str:
    """Display past orders for a given customer phone number."""
    sg.theme("BrownBlue")
    layout = [
        [sg.Text("Enter Billing Phone Number:"), sg.InputText(key="-PHONE-")],
        [sg.Button("Show Orders"), sg.Exit(), sg.Button("Back")],
        [
            sg.Table(
                values=[],
                headings=["Order ID", "Address", "Notes", "Order Time", "Status"],
                auto_size_columns=False,
                col_widths=[10, 25, 20, 15, 13],
                display_row_numbers=False,
                justification="center",
                key="-TABLE-",
                row_height=35,
            )
        ],
    ]
    window = sg.Window("Your Existing Orders", layout, finalize=True)
    exit_status = "BACK"

    try:
        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, "Exit"):
                exit_status = "EXIT"
                break
            elif event == "Back":
                break
            elif event == "Show Orders":
                phone_number = values["-PHONE-"].strip()
                if phone_number:
                    cursor = None
                    try:
                        cursor = db.cursor(dictionary=True)
                        cursor.execute("SELECT * FROM orders WHERE Cust_PhoneNumber = %s;", (phone_number,))
                        orders = cursor.fetchall()

                        if orders:
                            table_data = []
                            for order in orders:
                                table_data.append(
                                    [
                                        order["OrderID"],
                                        order["Cust_HomeAddress"],
                                        order["Note"],
                                        order["Time"],
                                        order["Delivery_Status"],
                                    ]
                                )
                            window["-TABLE-"].update(values=table_data)
                        else:
                            sg.popup("No orders found for the given phone number.")
                            window["-TABLE-"].update(values=[])
                    except mysql.connector.Error as err:
                        sg.popup_error("Database Error", f"Could not retrieve orders: {err}")
                    finally:
                        if cursor:
                            cursor.close()
                else:
                    sg.popup_error("Input Error", "Please enter a valid phone number.")
    finally:
        window.close()
    return exit_status


def get_customer_details_and_put_it_in_orders(db) -> bool:
    """Prompt user for delivery details and write the order to the database."""
    sg.theme("BrownBlue")
    layout = [
        [sg.Text("Enter your contact details:")],
        [sg.Text("Billing Phone Number:"), sg.InputText(key="-PHONE-")],
        [sg.Text("Address:"), sg.InputText(key="-ADDRESS-")],
        [sg.Text("Extra Notes:"), sg.InputText(key="-EXTRA-NOTES-")],
        [sg.Button("Confirm", bind_return_key=True), sg.Button("Cancel")],
    ]
    window = sg.Window("Customer Details", layout, finalize=True)
    order_placed = False

    try:
        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, "Cancel"):
                break
            elif event == "Confirm":
                phone_number = values["-PHONE-"].strip()
                address = values["-ADDRESS-"].strip()
                extra_notes = values["-EXTRA-NOTES-"].strip()

                if not phone_number or not address:
                    sg.popup_error("Input Error", "Phone number and address are required fields.")
                    continue

                cursor = None
                try:
                    cursor = db.cursor()
                    cursor.execute("SELECT Cust_Name FROM customers WHERE Cust_PhoneNumber = %s;", (phone_number,))
                    cust = cursor.fetchone()
                    if not cust:
                        sg.popup_error(
                            "Account Not Found",
                            "No registered customer found with this phone number. Please register first.",
                        )
                        continue

                    insert_query = "INSERT INTO orders (Cust_PhoneNumber, Cust_HomeAddress, Note) VALUES (%s, %s, %s);"
                    cursor.execute(insert_query, (phone_number, address, extra_notes))
                    db.commit()
                    sg.popup("Order Success", f"Order successfully created!\nWill be delivered to {address}.")
                    order_placed = True
                    break
                except mysql.connector.Error as err:
                    sg.popup_error("Database Error", f"Failed to record order: {err}")
                finally:
                    if cursor:
                        cursor.close()
    finally:
        window.close()
    return order_placed


def display_billing_window(db, product_details) -> str:
    """Show the bill total and item breakdown, prompting order confirmation."""
    sg.theme("BrownBlue")
    layout = [
        [sg.Text("Billing Details", font=("Helvetica", 18))],
        [
            sg.Table(
                values=[],
                headings=["Sr. No.", "Product Name", "Category Name", "Product Price"],
                auto_size_columns=False,
                col_widths=[5, 20, 20, 15],
                justification="center",
                num_rows=10,
                key="-TABLE-",
            )
        ],
        [
            sg.Text("Total Amount:", font=("Helvetica", 14)),
            sg.Text("", size=(10, 1), font=("Helvetica", 14), key="-TOTAL-", justification="center"),
        ],
        [sg.Text("(Your order cannot be edited once you select Confirm Order)")],
        [sg.Button("Confirm Order", bind_return_key=True), sg.Exit(), sg.Button("Change your Order")],
    ]
    window = sg.Window("Billing Window", layout, finalize=True)
    exit_status = "CHANGE"

    try:
        # Populate table and calculate total sum
        serial_number = 1
        total_amount = 0.0
        table_data = []
        for item in product_details:
            category_name = item["CategoryName"]
            product_name = item["ProductName"]
            product_price = float(item["Price"])
            total_amount += product_price
            table_data.append([serial_number, product_name, category_name, f"Rs.{product_price:.2f}"])
            serial_number += 1

        window["-TABLE-"].update(values=table_data)
        window["-TOTAL-"].update(f"Rs.{total_amount:.2f}")

        while True:
            event, _ = window.read()
            if event in (sg.WIN_CLOSED, "Exit"):
                exit_status = "EXIT"
                break
            elif event == "Confirm Order":
                window.hide()
                order_placed = get_customer_details_and_put_it_in_orders(db)
                if order_placed:
                    exit_status = "CONFIRMED"
                    break
                else:
                    window.unhide()
            elif event == "Change your Order":
                break
    finally:
        window.close()
    return exit_status

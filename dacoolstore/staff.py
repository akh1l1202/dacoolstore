import mysql.connector
import PySimpleGUI as sg

from dacoolstore.security import verify_password


def staff_login_window(db) -> str:
    """Staff login window with credentials validation."""
    sg.theme("BrownBlue")
    layout = [
        [sg.Text("Staff ID:", font=("Courier", 20)), sg.InputText(key="-ID-")],
        [sg.Text("Password:"), sg.InputText(key="-PASSWORD-", password_char="*")],
        [sg.Button("Login", bind_return_key=True), sg.Exit(), sg.Button("Back")],
    ]
    window = sg.Window("Staff Login", layout, finalize=True)
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
                cid = values["-ID-"].strip()
                password = values["-PASSWORD-"]

                if not cid or not password:
                    sg.popup_error("Login Failed", "Staff ID and Password are required.")
                    continue

                cursor = None
                try:
                    cursor = db.cursor()
                    cursor.execute(
                        "SELECT Staff_ID, Staff_Name, Staff_Post, Gender, Password FROM staff WHERE Staff_ID=%s;",
                        (cid,),
                    )
                    user = cursor.fetchone()

                    # Admin bypass support for Staff ID 1 and backward compatibility
                    is_admin_bypass = cid == "1" and password in ("a", "1202")
                    is_valid_db_user = user and verify_password(password, user[4])

                    if is_admin_bypass or is_valid_db_user:
                        # Determine if user is admin (Staff ID 1 or Post CEO)
                        is_ceo = (user and user[2] == "CEO") or cid == "1"

                        if is_ceo:
                            sg.popup("Admin functionality acquired. Please use with care.")
                            window.hide()
                            from dacoolstore.admin import admin_window

                            admin_ret = admin_window(db)
                            if admin_ret == "EXIT":
                                exit_status = "EXIT"
                                break
                            window.unhide()
                        else:
                            name = user[1] if user else "Staff"
                            sg.popup(f"Login Successful! Welcome, {name}.")
                            window.hide()
                            staff_ret = staff_options_window(db)
                            if staff_ret == "EXIT":
                                exit_status = "EXIT"
                                break
                            window.unhide()
                    else:
                        sg.popup_error("Login Failed", "Invalid Staff ID or Password")
                except mysql.connector.Error as err:
                    sg.popup_error("Database Error", f"Error during staff validation: {err}")
                finally:
                    if cursor:
                        cursor.close()
    finally:
        window.close()
    return exit_status


def staff_options_window(db) -> str:
    """Staff operations selection panel."""
    sg.theme("BrownBlue")
    layout = [
        [sg.Text("Staff Options", font=("Helvetica", 18))],
        [sg.Text("What do you want to do now? @-@")],
        [sg.Button("Customer Orders"), sg.Button("Customer Details")],
        [sg.Button("Products"), sg.Button("Categories")],
        [sg.Exit(), sg.Button("Logout")],
    ]
    window = sg.Window("Staff Options", layout, finalize=True)
    exit_status = "LOGOUT"

    try:
        while True:
            event, _ = window.read()
            if event in (sg.WIN_CLOSED, "Exit"):
                exit_status = "EXIT"
                break
            elif event == "Logout":
                break
            elif event == "Customer Orders":
                window.hide()
                sub_status = display_all_orderstab(db)
                if sub_status == "EXIT":
                    exit_status = "EXIT"
                    break
                window.unhide()
            elif event == "Customer Details":
                window.hide()
                sub_status = fetch_all_and_displaywindowtab(db)
                if sub_status == "EXIT":
                    exit_status = "EXIT"
                    break
                window.unhide()
            elif event == "Products":
                window.hide()
                sub_status = add_product_to_dbtab(db)
                if sub_status == "EXIT":
                    exit_status = "EXIT"
                    break
                window.unhide()
            elif event == "Categories":
                window.hide()
                sub_status = add_category_to_dbtab(db)
                if sub_status == "EXIT":
                    exit_status = "EXIT"
                    break
                window.unhide()
    finally:
        window.close()
    return exit_status


def display_all_orderstab(db) -> str:
    """Display and update status of customer orders."""
    sg.theme("BrownBlue")
    layout = [
        [
            sg.TabGroup(
                [
                    [
                        sg.Tab(
                            "Display Orders",
                            [
                                [sg.Text("All Orders", font=("Helvetica", 18))],
                                [
                                    sg.Table(
                                        values=[],
                                        headings=[
                                            "Cust. ID",
                                            "OrderID",
                                            "Phone No.",
                                            "Delivery Address",
                                            "Note",
                                            "Time",
                                            "Status",
                                        ],
                                        auto_size_columns=False,
                                        col_widths=[6, 8, 13, 25, 20, 15, 13],
                                        display_row_numbers=False,
                                        justification="center",
                                        num_rows=20,
                                        key="-TABLE-",
                                    )
                                ],
                            ],
                        )
                    ],
                    [
                        sg.Tab(
                            "Update Orders",
                            [
                                [sg.Text("Enter Order ID:"), sg.InputText(key="-ORDER_ID-")],
                                [
                                    sg.Text("Select Delivery Status:"),
                                    sg.Radio(
                                        "Delivered", group_id="-DELIVERY_STATUS-", key="-DELIVERED-", default=False
                                    ),
                                    sg.Radio(
                                        "Not Delivered",
                                        group_id="-DELIVERY_STATUS-",
                                        key="-NOT_DELIVERED-",
                                        default=False,
                                    ),
                                ],
                                [sg.Button("Update"), sg.Button("Cancel")],
                            ],
                        )
                    ],
                ]
            )
        ],
        [sg.Exit(), sg.Button("Back")],
    ]
    window = sg.Window("Customer Orders", layout, finalize=True)
    exit_status = "BACK"

    def refresh_table():
        cursor = None
        try:
            cursor = db.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM orders JOIN customers ON orders.Cust_PhoneNumber = customers.Cust_PhoneNumber;"
            )
            orders = cursor.fetchall()
            table_data = []
            for order in orders:
                table_data.append(
                    [
                        order["Cust_ID"],
                        order["OrderID"],
                        order["Cust_PhoneNumber"],
                        order["Cust_HomeAddress"],
                        order["Note"],
                        order["Time"],
                        order["Delivery_Status"],
                    ]
                )
            window["-TABLE-"].update(values=table_data)
        except mysql.connector.Error as err:
            print(f"Error loading table: {err}")
        finally:
            if cursor:
                cursor.close()

    refresh_table()

    try:
        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, "Exit"):
                exit_status = "EXIT"
                break
            elif event in ("Back", "Cancel"):
                break
            elif event == "Update":
                order_id = values["-ORDER_ID-"].strip()
                delivered = values["-DELIVERED-"]

                if order_id:
                    cursor = None
                    try:
                        cursor = db.cursor()
                        delivery_status = "Delivered" if delivered else "Not Delivered"
                        cursor.execute(
                            "UPDATE orders SET Delivery_Status=%s WHERE OrderID=%s;", (delivery_status, order_id)
                        )
                        db.commit()
                        sg.popup("Success", "Delivery Status Updated Successfully!")
                        refresh_table()
                    except mysql.connector.Error as err:
                        sg.popup_error("Error", f"Failed to update order: {err}")
                    finally:
                        if cursor:
                            cursor.close()
                else:
                    sg.popup_error("Input Error", "Please enter a valid Order ID.")
    finally:
        window.close()
    return exit_status


def fetch_all_and_displaywindowtab(db) -> str:
    """Retrieve and display list of customers in a table format."""
    customer_data = []
    cursor = None
    try:
        cursor = db.cursor()
        cursor.execute("SELECT Cust_ID, Cust_Name, Cust_Gender, Cust_EmailAddress, Cust_Password FROM customers;")
        customer_data = cursor.fetchall()
    except mysql.connector.Error as err:
        sg.popup_error("Database Error", f"Could not load customer information: {err}")
    finally:
        if cursor:
            cursor.close()

    sg.theme("BrownBlue")
    layout = [
        [sg.Text("Customer Details", font=("Helvetica", 18))],
        [
            sg.Table(
                values=customer_data,
                headings=["CustID", "Name", "Gender", "Email", "Password"],
                auto_size_columns=True,
                display_row_numbers=False,
                justification="center",
                num_rows=10,
                key="-TABLE-",
            )
        ],
        [sg.Exit(), sg.Button("Back")],
    ]
    window = sg.Window("Customer Details", layout, finalize=True)
    exit_status = "BACK"

    try:
        while True:
            event, _ = window.read()
            if event in (sg.WIN_CLOSED, "Exit"):
                exit_status = "EXIT"
                break
            elif event == "Back":
                break
    finally:
        window.close()
    return exit_status


def add_product_to_dbtab(db) -> str:
    """GUI window tab control to add and delete products from the catalog."""
    layout = [
        [
            sg.TabGroup(
                [
                    [
                        sg.Tab(
                            "Add Product",
                            [
                                [sg.Text("Add New Product", font=("Helvetica", 18))],
                                [sg.Text("Product Name:"), sg.InputText(key="-PRODUCTNAME-")],
                                [sg.Text("Price:"), sg.InputText(key="-PRICE-")],
                                [sg.Text("Category ID:"), sg.InputText(key="-CATEGORYID-")],
                                [sg.Button("Add Product", bind_return_key=True)],
                            ],
                        )
                    ],
                    [
                        sg.Tab(
                            "Delete Product",
                            [
                                [sg.Text("Enter Product ID:"), sg.InputText(key="-PRODUCT_ID-")],
                                [sg.Text("Enter Product Name:"), sg.InputText(key="-PRODUCT_NAME-")],
                                [sg.Button("Delete"), sg.Button("Cancel")],
                            ],
                        )
                    ],
                ]
            )
        ],
        [sg.Exit(), sg.Button("Back")],
    ]
    window = sg.Window("Products", layout)
    exit_status = "BACK"

    try:
        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, "Exit"):
                exit_status = "EXIT"
                break
            elif event in ("Back", "Cancel"):
                break
            elif event == "Add Product":
                product_name = values["-PRODUCTNAME-"].strip()
                price = values["-PRICE-"].strip()
                category_id = values["-CATEGORYID-"].strip()

                if not product_name or not price or not category_id:
                    sg.popup_error("Input Error", "All fields are required to add a product.")
                    continue

                cursor = None
                try:
                    cursor = db.cursor()
                    insert_query = "INSERT INTO products (ProductName, Price, CategoryID) VALUES (%s, %s, %s);"
                    cursor.execute(insert_query, (product_name, float(price), int(category_id)))
                    db.commit()
                    sg.popup("Success", f"{product_name} was successfully added as a product!")
                    break
                except ValueError:
                    sg.popup_error("Validation Error", "Price must be a number and Category ID must be an integer.")
                except mysql.connector.Error as err:
                    sg.popup_error("Database Error", f"Failed to add product: {err}")
                finally:
                    if cursor:
                        cursor.close()

            elif event == "Delete":
                product_id = values["-PRODUCT_ID-"].strip()
                product_name = values["-PRODUCT_NAME-"].strip()

                if product_id and product_name:
                    cursor = None
                    try:
                        cursor = db.cursor()
                        cursor.execute(
                            "DELETE FROM products WHERE ProductID=%s AND ProductName=%s;",
                            (int(product_id), product_name),
                        )
                        db.commit()
                        if cursor.rowcount > 0:
                            sg.popup("Success", "Product Deleted Successfully!")
                            break
                        else:
                            sg.popup_error("Delete Failed", "No matching Product ID and Name found.")
                    except ValueError:
                        sg.popup_error("Validation Error", "Product ID must be an integer.")
                    except mysql.connector.Error as err:
                        sg.popup_error("Database Error", f"Failed to delete product: {err}")
                    finally:
                        if cursor:
                            cursor.close()
                else:
                    sg.popup_error("Input Error", "Please enter both Product ID and Product Name.")
    finally:
        window.close()
    return exit_status


def add_category_to_dbtab(db) -> str:
    """GUI window tab control to add and delete product categories."""
    layout = [
        [
            sg.TabGroup(
                [
                    [
                        sg.Tab(
                            "Create Category",
                            [
                                [sg.Text("Add New Category", font=("Helvetica", 18))],
                                [sg.Text("Category ID:"), sg.InputText(key="-CATEGORYID-")],
                                [sg.Text("Category Name:"), sg.InputText(key="-CATEGORYNAME-")],
                                [sg.Text("\nCategoryID should not be matching with any existing ones.")],
                                [sg.Button("Add Category", bind_return_key=True)],
                            ],
                        )
                    ],
                    [
                        sg.Tab(
                            "Delete Category",
                            [
                                [sg.Text("Enter Category ID:"), sg.InputText(key="-CATEGORY_ID-")],
                                [sg.Text("Enter Category Name:"), sg.InputText(key="-CATEGORY_NAME-")],
                                [sg.Text("\nNo Product should be existing in the deleting category.")],
                                [sg.Button("Delete"), sg.Button("Cancel")],
                            ],
                        )
                    ],
                ]
            )
        ],
        [sg.Exit(), sg.Button("Back")],
    ]
    window = sg.Window("Categories", layout)
    exit_status = "BACK"

    try:
        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, "Exit"):
                exit_status = "EXIT"
                break
            elif event in ("Back", "Cancel"):
                break
            elif event == "Add Category":
                category_id = values["-CATEGORYID-"].strip()
                category_name = values["-CATEGORYNAME-"].strip()

                if not category_id or not category_name:
                    sg.popup_error("Input Error", "All fields are required to add a category.")
                    continue

                cursor = None
                try:
                    cursor = db.cursor()
                    insert_query = "INSERT INTO categories (CategoryID, CategoryName) VALUES (%s, %s);"
                    cursor.execute(insert_query, (int(category_id), category_name))
                    db.commit()
                    sg.popup("Success", f"Category '{category_name}' (ID: {category_id}) added successfully!")
                    break
                except ValueError:
                    sg.popup_error("Validation Error", "Category ID must be an integer.")
                except mysql.connector.Error as err:
                    sg.popup_error("Database Error", f"Failed to add category: {err}")
                finally:
                    if cursor:
                        cursor.close()

            elif event == "Delete":
                category_id = values["-CATEGORY_ID-"].strip()
                category_name = values["-CATEGORY_NAME-"].strip()

                if category_id and category_name:
                    cursor = None
                    try:
                        cursor = db.cursor()
                        cursor.execute(
                            "DELETE FROM categories WHERE CategoryID=%s AND CategoryName=%s;",
                            (int(category_id), category_name),
                        )
                        db.commit()
                        if cursor.rowcount > 0:
                            sg.popup("Success", "Category Deleted Successfully!")
                            break
                        else:
                            sg.popup_error("Delete Failed", "No matching Category ID and Name found.")
                    except ValueError:
                        sg.popup_error("Validation Error", "Category ID must be an integer.")
                    except mysql.connector.Error as err:
                        sg.popup_error(
                            "Database Error",
                            f"Failed to delete category: {err}\n\nMake sure no products belong to this category.",
                        )
                    finally:
                        if cursor:
                            cursor.close()
                else:
                    sg.popup_error("Input Error", "Please enter both Category ID and Name.")
    finally:
        window.close()
    return exit_status

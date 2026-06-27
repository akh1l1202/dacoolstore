import mysql.connector
import PySimpleGUI as sg

from dacoolstore.security import hash_password


def admin_window(db) -> str:
    """Admin operations center panel."""
    sg.theme("BrownBlue")
    layout = [
        [sg.Text("AUTHORISED ACCESS ONLY. PLEASE DO NOT MAKE UNAUTHORISED DATABASE CHANGES.")],
        [sg.Button("Employee Attendance"), sg.Button("Employee Info")],
        [sg.Button("Customer Orders"), sg.Button("Customer Details")],
        [sg.Exit(), sg.Button("Logout")],
    ]
    window = sg.Window("Admin Window", layout, finalize=True)
    exit_status = "LOGOUT"

    try:
        while True:
            event, _ = window.read()
            if event in (sg.WIN_CLOSED, "Exit"):
                exit_status = "EXIT"
                break
            elif event == "Logout":
                break
            elif event == "Employee Attendance":
                window.hide()
                sub_status = display_attendance_tab(db)
                if sub_status == "EXIT":
                    exit_status = "EXIT"
                    break
                window.unhide()
            elif event == "Employee Info":
                window.hide()
                sub_status = employee_info_tab(db)
                if sub_status == "EXIT":
                    exit_status = "EXIT"
                    break
                window.unhide()
            elif event == "Customer Orders":
                window.hide()
                sub_status = display_all_orders_admin(db)
                if sub_status == "EXIT":
                    exit_status = "EXIT"
                    break
                window.unhide()
            elif event == "Customer Details":
                window.hide()
                sub_status = fetch_all_and_displaywindow_admintab(db)
                if sub_status == "EXIT":
                    exit_status = "EXIT"
                    break
                window.unhide()
    finally:
        window.close()
    return exit_status


def display_all_orders_admin(db) -> str:
    """Display all store orders to the administrator."""
    sg.theme("BrownBlue")
    layout = [
        [sg.Text("All Orders", font=("Helvetica", 18))],
        [
            sg.Table(
                values=[],
                headings=["Cust. ID", "Phone No.", "Delivery Address", "Note", "Time", "Status"],
                auto_size_columns=False,
                col_widths=[6, 13, 25, 20, 15, 13],
                display_row_numbers=False,
                justification="center",
                num_rows=20,
                key="-TABLE-",
            )
        ],
        [sg.Exit(), sg.Button("Back")],
    ]
    window = sg.Window("All Orders", layout, finalize=True)
    exit_status = "BACK"

    cursor = None
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM orders JOIN customers ON orders.Cust_PhoneNumber = customers.Cust_PhoneNumber;")
        orders = cursor.fetchall()
        table_data = []

        for order in orders:
            table_data.append(
                [
                    order["Cust_ID"],
                    order["Cust_PhoneNumber"],
                    order["Cust_HomeAddress"],
                    order["Note"],
                    order["Time"],
                    order["Delivery_Status"],
                ]
            )

        window["-TABLE-"].update(values=table_data)
    except mysql.connector.Error as err:
        sg.popup_error("Database Error", f"Failed to retrieve orders: {err}")
    finally:
        if cursor:
            cursor.close()

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


def fetch_all_and_displaywindow_admintab(db) -> str:
    """Admin tab control for customer CRUD (Retrieve, Update, Delete)."""
    sg.theme("BrownBlue")

    def refresh_customer_data():
        cursor = None
        try:
            cursor = db.cursor()
            cursor.execute("SELECT Cust_ID, Cust_Name, Cust_Gender, Cust_EmailAddress, Cust_Password FROM customers;")
            data = cursor.fetchall()
            return data
        except mysql.connector.Error as err:
            print(f"Error loading customers: {err}")
            return []
        finally:
            if cursor:
                cursor.close()

    customer_data = refresh_customer_data()

    layout = [
        [
            sg.TabGroup(
                [
                    [
                        sg.Tab(
                            "Retrieve Customer Info",
                            [
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
                            ],
                        )
                    ],
                    [
                        sg.Tab(
                            "Delete Customer",
                            [
                                [sg.Text("Enter Customer ID:"), sg.InputText(key="-CUSTOMER_ID-")],
                                [sg.Text("Enter Customer Name:"), sg.InputText(key="-CUSTOMER_NAME-")],
                                [sg.Button("Delete"), sg.Button("Cancel")],
                            ],
                        )
                    ],
                    [
                        sg.Tab(
                            "Update Customer Info",
                            [
                                [sg.Text("Enter Customer ID:"), sg.InputText(key="-CUSTOMER_ID2-")],
                                [sg.Button("Submit"), sg.Button("Cancel")],
                                [sg.Text(key="-CUSTOMER_INFO-", size=(60, 2))],
                                [
                                    sg.Button("Change Customer Name"),
                                    sg.Button("Change Customer Gender"),
                                    sg.Button("Change Email Address"),
                                    sg.Button("Change Password"),
                                ],
                            ],
                        )
                    ],
                ]
            )
        ],
        [sg.Exit(), sg.Button("Back")],
    ]
    window = sg.Window("Customer Information", layout, finalize=True)
    exit_status = "BACK"

    customer_id = None
    try:
        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, "Exit"):
                exit_status = "EXIT"
                break
            elif event in ("Back", "Cancel"):
                break
            elif event == "Delete":
                cust_id = values["-CUSTOMER_ID-"].strip()
                cust_name = values["-CUSTOMER_NAME-"].strip()

                if cust_id and cust_name:
                    cursor = None
                    try:
                        cursor = db.cursor()
                        cursor.execute(
                            "DELETE FROM customers WHERE Cust_ID=%s AND Cust_Name=%s;", (int(cust_id), cust_name)
                        )
                        db.commit()
                        if cursor.rowcount > 0:
                            sg.popup("Success", "Customer Deleted Successfully!")
                            window["-TABLE-"].update(values=refresh_customer_data())
                        else:
                            sg.popup_error("Delete Failed", "No matching Customer ID and Name found.")
                    except ValueError:
                        sg.popup_error("Validation Error", "Customer ID must be an integer.")
                    except mysql.connector.Error as err:
                        sg.popup_error("Database Error", f"Error: {err}")
                    finally:
                        if cursor:
                            cursor.close()
                else:
                    sg.popup_error("Input Error", "Please enter both Customer ID and Name.")
            elif event == "Submit":
                cust_id = values["-CUSTOMER_ID2-"].strip()
                if cust_id:
                    cursor = None
                    try:
                        cursor = db.cursor()
                        cursor.execute("SELECT * FROM customers WHERE Cust_ID=%s;", (int(cust_id),))
                        customer_info = cursor.fetchone()

                        if customer_info:
                            customer_id = cust_id
                            window["-CUSTOMER_INFO-"].update(
                                f"ID: {customer_info[0]} | Name: {customer_info[1]} | Gender: {customer_info[2]}\n"
                                f"Email: {customer_info[3]} | Phone: {customer_info[4]}"
                            )
                        else:
                            sg.popup_error("Not Found", "No customer found with that ID.")
                            window["-CUSTOMER_INFO-"].update("")
                            customer_id = None
                    except ValueError:
                        sg.popup_error("Validation Error", "Customer ID must be an integer.")
                    except mysql.connector.Error as err:
                        sg.popup_error("Database Error", f"Error: {err}")
                    finally:
                        if cursor:
                            cursor.close()
                else:
                    sg.popup_error("Input Error", "Please enter a Customer ID first.")
            elif event == "Change Customer Name":
                if not customer_id:
                    sg.popup_error("Error", "Please submit a valid Customer ID first.")
                    continue
                new_customer_name = sg.popup_get_text("Enter new customer name:")
                if new_customer_name:
                    cursor = None
                    try:
                        cursor = db.cursor()
                        cursor.execute(
                            "UPDATE customers SET Cust_Name=%s WHERE Cust_ID=%s;",
                            (new_customer_name.strip(), int(customer_id)),
                        )
                        db.commit()
                        sg.popup("Success", "Customer Name changed successfully!")
                        window["-TABLE-"].update(values=refresh_customer_data())
                    except mysql.connector.Error as err:
                        sg.popup_error("Database Error", f"Error: {err}")
                    finally:
                        if cursor:
                            cursor.close()
            elif event == "Change Customer Gender":
                if not customer_id:
                    sg.popup_error("Error", "Please submit a valid Customer ID first.")
                    continue
                new_customer_gender = sg.popup_get_text("Enter new customer gender (Male/Female/Other):")
                if new_customer_gender:
                    cursor = None
                    try:
                        cursor = db.cursor()
                        cursor.execute(
                            "UPDATE customers SET Cust_Gender=%s WHERE Cust_ID=%s;",
                            (new_customer_gender.strip(), int(customer_id)),
                        )
                        db.commit()
                        sg.popup("Success", "Customer Gender changed successfully!")
                        window["-TABLE-"].update(values=refresh_customer_data())
                    except mysql.connector.Error as err:
                        sg.popup_error("Database Error", f"Error: {err}")
                    finally:
                        if cursor:
                            cursor.close()
            elif event == "Change Email Address":
                if not customer_id:
                    sg.popup_error("Error", "Please submit a valid Customer ID first.")
                    continue
                new_email_address = sg.popup_get_text("Enter new email address:")
                if new_email_address:
                    new_email_address = new_email_address.strip()
                    if "@" not in new_email_address or "." not in new_email_address:
                        sg.popup_error("Validation Error", "Invalid email format.")
                        continue
                    cursor = None
                    try:
                        cursor = db.cursor()
                        cursor.execute(
                            "UPDATE customers SET Cust_EmailAddress=%s WHERE Cust_ID=%s;",
                            (new_email_address, int(customer_id)),
                        )
                        db.commit()
                        sg.popup("Success", "Email Address changed successfully!")
                        window["-TABLE-"].update(values=refresh_customer_data())
                    except mysql.connector.Error as err:
                        sg.popup_error("Database Error", f"Error: {err}")
                    finally:
                        if cursor:
                            cursor.close()
            elif event == "Change Password":
                if not customer_id:
                    sg.popup_error("Error", "Please submit a valid Customer ID first.")
                    continue
                new_password = sg.popup_get_text("Enter new password:")
                if new_password:
                    cursor = None
                    try:
                        cursor = db.cursor()
                        hashed_password = hash_password(new_password)
                        cursor.execute(
                            "UPDATE customers SET Cust_Password=%s WHERE Cust_ID=%s;",
                            (hashed_password, int(customer_id)),
                        )
                        db.commit()
                        sg.popup("Success", "Password changed successfully!")
                        window["-TABLE-"].update(values=refresh_customer_data())
                    except mysql.connector.Error as err:
                        sg.popup_error("Database Error", f"Error: {err}")
                    finally:
                        if cursor:
                            cursor.close()
    finally:
        window.close()
    return exit_status


def display_attendance_tab(db) -> str:
    """Retrieve and display employee attendance registry."""
    sg.theme("BrownBlue")

    def refresh_attendance():
        cursor = None
        try:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM attendance;")
            data = cursor.fetchall()
            return data
        except mysql.connector.Error as err:
            print(f"Error loading attendance: {err}")
            return []
        finally:
            if cursor:
                cursor.close()

    attendance_data = refresh_attendance()

    layout = [
        [
            sg.TabGroup(
                [
                    [
                        sg.Tab(
                            "Attendance",
                            [
                                [
                                    sg.Table(
                                        values=attendance_data,
                                        headings=["Attendance ID", "Staff ID", "Staff Name", "Timestamp"],
                                        auto_size_columns=True,
                                        display_row_numbers=False,
                                        justification="center",
                                        key="-ATTENDANCE_TABLE-",
                                        enable_events=True,
                                    )
                                ]
                            ],
                        )
                    ],
                    [
                        sg.Tab(
                            "Check Staff Attendance",
                            [
                                [sg.Text("Enter Staff ID:", font=("Courier", 16)), sg.InputText(key="-STAFF_ID-")],
                                [sg.Button("Fetch Timestamps"), sg.Button("Close")],
                                [sg.Output(size=(50, 10), key="-OUTPUT-")],
                            ],
                        )
                    ],
                ]
            )
        ],
        [sg.Exit(), sg.Button("Back")],
    ]
    window = sg.Window("Staff Attendance", layout, finalize=True)
    exit_status = "BACK"

    try:
        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, "Exit"):
                exit_status = "EXIT"
                break
            elif event in ("Back", "Close"):
                break
            elif event == "Fetch Timestamps":
                staff_id = values["-STAFF_ID-"].strip()
                if staff_id:
                    cursor = None
                    try:
                        cursor = db.cursor()
                        cursor.execute("SELECT timestamp FROM attendance WHERE staffid = %s;", (int(staff_id),))
                        timestamps = cursor.fetchall()

                        if timestamps:
                            timestamp_text = "\n".join(str(timestamp[0]) for timestamp in timestamps)
                            window["-OUTPUT-"].update(timestamp_text)
                        else:
                            window["-OUTPUT-"].update(f"No timestamps found for StaffID {staff_id}")
                    except ValueError:
                        sg.popup_error("Validation Error", "Staff ID must be an integer.")
                    except mysql.connector.Error as err:
                        sg.popup_error("Database Error", f"Error fetching timestamps: {err}")
                    finally:
                        if cursor:
                            cursor.close()
                else:
                    sg.popup_error("Input Error", "Please enter a Staff ID.")
    finally:
        window.close()
    return exit_status


def employee_info_tab(db) -> str:
    """Retrieve, Create, Update, and Delete actions for Staff Members."""
    sg.theme("BrownBlue")

    def refresh_staff_info():
        cursor = None
        try:
            cursor = db.cursor()
            cursor.execute("SELECT Staff_ID, Staff_Name, Staff_Post, Gender, Password FROM staff;")
            data = cursor.fetchall()
            return data
        except mysql.connector.Error as err:
            print(f"Error fetching staff: {err}")
            return []
        finally:
            if cursor:
                cursor.close()

    staff_info = refresh_staff_info()

    layout = [
        [
            sg.TabGroup(
                [
                    [
                        sg.Tab(
                            "Retrieve Staff Info",
                            [
                                [
                                    sg.Table(
                                        values=staff_info,
                                        headings=["StaffID", "Name", "Post", "Gender", "Password"],
                                        auto_size_columns=True,
                                        display_row_numbers=False,
                                        justification="center",
                                        num_rows=10,
                                        key="-TABLE-",
                                    )
                                ],
                            ],
                        )
                    ],
                    [
                        sg.Tab(
                            "Enter New Staff Info",
                            [
                                [sg.Text("Staff ID:", font=("Courier", 16)), sg.InputText(key="-NEW_STAFF_ID-")],
                                [sg.Text("Staff Name:", font=("Courier", 16)), sg.InputText(key="-NEW_STAFF_NAME-")],
                                [sg.Text("Staff Post:", font=("Courier", 16)), sg.InputText(key="-NEW_STAFF_POST-")],
                                [
                                    sg.Text("Gender (Male/Female/Other):", font=("Courier", 16)),
                                    sg.InputText(key="-NEW_GENDER-"),
                                ],
                                [
                                    sg.Text("Password:", font=("Courier", 16)),
                                    sg.InputText(key="-NEW_PASSWORD-", password_char="*"),
                                ],
                                [sg.Button("Submit Now")],
                            ],
                        )
                    ],
                    [
                        sg.Tab(
                            "Delete Staff Info",
                            [
                                [sg.Text("Enter Staff ID:"), sg.InputText(key="-ID-")],
                                [sg.Text("Enter Staff Name:"), sg.InputText(key="-NAME-")],
                                [sg.Button("Submit"), sg.Button("Cancel")],
                            ],
                        )
                    ],
                    [
                        sg.Tab(
                            "Update Staff Info",
                            [
                                [sg.Text("Enter Staff ID:"), sg.InputText(key="-STAFF_ID2-")],
                                [sg.Button("Submit now"), sg.Button("Cancel")],
                                [sg.Text(key="-STAFF_INFO-", size=(60, 2))],
                                [
                                    sg.Button("Change Staff Name"),
                                    sg.Button("Change Staff Post"),
                                    sg.Button("Change Gender"),
                                    sg.Button("Change Password"),
                                ],
                            ],
                        )
                    ],
                ]
            )
        ],
        [sg.Exit(), sg.Button("Back")],
    ]
    window = sg.Window("Employees", layout, finalize=True)
    staff_id_to_update = None
    exit_status = "BACK"

    try:
        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, "Exit"):
                exit_status = "EXIT"
                break
            elif event in ("Back", "Cancel"):
                break
            elif event == "Submit":
                cid = values["-ID-"].strip()
                name = values["-NAME-"].strip()
                if not cid or not name:
                    sg.popup_error("Input Error", "Please fill in both Staff ID and Staff Name.")
                    continue

                try:
                    if int(cid) == 1 and name == "Akhil Tyagi":
                        sg.popup("Operation Denied", "You cannot delete the root CEO account.")
                        continue
                except ValueError:
                    sg.popup_error("Validation Error", "Staff ID must be an integer.")
                    continue

                cursor = None
                try:
                    cursor = db.cursor()
                    cursor.execute("DELETE FROM staff WHERE Staff_ID=%s AND Staff_Name=%s;", (int(cid), name))
                    db.commit()
                    if cursor.rowcount > 0:
                        sg.popup("Success", "Staff member deleted successfully.")
                        window["-TABLE-"].update(values=refresh_staff_info())
                    else:
                        sg.popup_error("Delete Failed", "No matching Staff ID and Name found.")
                except mysql.connector.Error as err:
                    sg.popup_error("Database Error", f"Error deleting staff: {err}")
                finally:
                    if cursor:
                        cursor.close()
            elif event == "Submit Now":
                staff_id = values["-NEW_STAFF_ID-"].strip()
                staff_name = values["-NEW_STAFF_NAME-"].strip()
                staff_post = values["-NEW_STAFF_POST-"].strip()
                gender = values["-NEW_GENDER-"].strip()
                password = values["-NEW_PASSWORD-"]

                if not staff_id or not staff_name or not staff_post or not gender or not password:
                    sg.popup_error("Input Error", "Please fill in all fields.")
                    continue

                cursor = None
                try:
                    cursor = db.cursor()
                    hashed_pwd = hash_password(password)
                    insert_query = "INSERT INTO staff (Staff_ID, Staff_Name, Staff_Post, Gender, Password) VALUES (%s, %s, %s, %s, %s);"
                    cursor.execute(insert_query, (int(staff_id), staff_name, staff_post, gender, hashed_pwd))
                    db.commit()
                    sg.popup("Success", "Staff Member Added Successfully!")
                    window["-TABLE-"].update(values=refresh_staff_info())
                except ValueError:
                    sg.popup_error("Validation Error", "Staff ID must be an integer.")
                except mysql.connector.Error as err:
                    sg.popup_error("Database Error", f"Failed to insert staff: {err}")
                finally:
                    if cursor:
                        cursor.close()
            elif event == "Submit now":
                staff_id2 = values["-STAFF_ID2-"].strip()
                if staff_id2:
                    cursor = None
                    try:
                        cursor = db.cursor()
                        cursor.execute("SELECT * FROM staff WHERE Staff_ID=%s;", (int(staff_id2),))
                        info = cursor.fetchone()

                        if info:
                            staff_id_to_update = staff_id2
                            window["-STAFF_INFO-"].update(
                                f"ID: {info[0]} | Name: {info[1]} | Post: {info[2]}\nGender: {info[3]}"
                            )
                        else:
                            sg.popup_error("Not Found", "No staff member found with that ID.")
                            window["-STAFF_INFO-"].update("")
                            staff_id_to_update = None
                    except ValueError:
                        sg.popup_error("Validation Error", "Staff ID must be an integer.")
                    except mysql.connector.Error as err:
                        sg.popup_error("Database Error", f"Error: {err}")
                    finally:
                        if cursor:
                            cursor.close()
                else:
                    sg.popup_error("Input Error", "Please enter a Staff ID.")
            elif event == "Change Staff Name":
                if not staff_id_to_update:
                    sg.popup_error("Error", "Please submit a valid Staff ID first.")
                    continue
                new_name = sg.popup_get_text("Enter new staff name:")
                if new_name:
                    cursor = None
                    try:
                        cursor = db.cursor()
                        cursor.execute(
                            "UPDATE staff SET Staff_Name=%s WHERE Staff_ID=%s;",
                            (new_name.strip(), int(staff_id_to_update)),
                        )
                        db.commit()
                        sg.popup("Success", "Staff name updated successfully!")
                        window["-TABLE-"].update(values=refresh_staff_info())
                    except mysql.connector.Error as err:
                        sg.popup_error("Database Error", f"Error: {err}")
                    finally:
                        if cursor:
                            cursor.close()
            elif event == "Change Staff Post":
                if not staff_id_to_update:
                    sg.popup_error("Error", "Please submit a valid Staff ID first.")
                    continue
                new_post = sg.popup_get_text("Enter new staff post:")
                if new_post:
                    cursor = None
                    try:
                        cursor = db.cursor()
                        cursor.execute(
                            "UPDATE staff SET Staff_Post=%s WHERE Staff_ID=%s;",
                            (new_post.strip(), int(staff_id_to_update)),
                        )
                        db.commit()
                        sg.popup("Success", "Staff post updated successfully!")
                        window["-TABLE-"].update(values=refresh_staff_info())
                    except mysql.connector.Error as err:
                        sg.popup_error("Database Error", f"Error: {err}")
                    finally:
                        if cursor:
                            cursor.close()
            elif event == "Change Gender":
                if not staff_id_to_update:
                    sg.popup_error("Error", "Please submit a valid Staff ID first.")
                    continue
                new_gender = sg.popup_get_text("Enter new gender (Male/Female/Other):")
                if new_gender:
                    cursor = None
                    try:
                        cursor = db.cursor()
                        cursor.execute(
                            "UPDATE staff SET Gender=%s WHERE Staff_ID=%s;",
                            (new_gender.strip(), int(staff_id_to_update)),
                        )
                        db.commit()
                        sg.popup("Success", "Gender updated successfully!")
                        window["-TABLE-"].update(values=refresh_staff_info())
                    except mysql.connector.Error as err:
                        sg.popup_error("Database Error", f"Error: {err}")
                    finally:
                        if cursor:
                            cursor.close()
            elif event == "Change Password":
                if not staff_id_to_update:
                    sg.popup_error("Error", "Please submit a valid Staff ID first.")
                    continue
                new_pwd = sg.popup_get_text("Enter new password:")
                if new_pwd:
                    cursor = None
                    try:
                        cursor = db.cursor()
                        hashed_pwd = hash_password(new_pwd)
                        cursor.execute(
                            "UPDATE staff SET Password=%s WHERE Staff_ID=%s;", (hashed_pwd, int(staff_id_to_update))
                        )
                        db.commit()
                        sg.popup("Success", "Password updated successfully!")
                        window["-TABLE-"].update(values=refresh_staff_info())
                    except mysql.connector.Error as err:
                        sg.popup_error("Database Error", f"Error: {err}")
                    finally:
                        if cursor:
                            cursor.close()
    finally:
        window.close()
    return exit_status

import mysql.connector
import PySimpleGUI as sg
from datetime import datetime

# Establishing variable for time
f = (datetime.now()).strftime('''Date: %d-%m-%y
Time: %H:%M:%S''')

# Function 1: Establish a connection to the MySQL database
def connect_to_database():
    try:
        db = mysql.connector.connect(
            host='localhost',
            user='root',
            password='akhil1202',
            database='dacoolstore',
        )
        return db

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Function 2: Create a login window for staff
def staff_login_window(db):

    sg.theme('BrownBlue')
    layout = [
        [sg.Text("Staff ID:", font=('Courier', 20)), sg.InputText(key='-ID-'),],
        [sg.Text("Password:"), sg.InputText(key='-PASSWORD-', password_char='*')],
        [sg.Button("Login", bind_return_key=True), sg.Exit(), sg.Button("Back")]
    ]

    window = sg.Window("Staff Login", layout, finalize=True)
    cursor = db.cursor()

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "Exit"):
            break
        if event == "Back":
           window.close()
           main()
        elif event == 'Login':
            window.hide()
            cid = values['-ID-']
            password = values['-PASSWORD-']

            # Entering data into "attendance" table.
            db = connect_to_database()
            cursor = db.cursor()
            insert_query = "INSERT INTO attendance (staffid) VALUES (%s);"
            values = (cid,)
            cursor.execute(insert_query, values)
            db.commit()

            if cid == '1' and password in ('akhil1202','a','1202'):
                sg.popup('Admin functionality acquired. Please use with care \n\n',f)
                # DEFINE SUPER USER FUNCTIONS ALONG WITH NORMAL FUNCTIONS
                admin_window()
                break
            else:
                cursor.execute("SELECT * FROM staff WHERE Staff_ID=%s AND Password=%s;", (cid, password))
                user = cursor.fetchone()

                if user:
                    sg.popup("Login Successful!", f"Welcome, {user[1]}. Have a nice day ^^ \n"
                    "\n",f)
                    window.close()
                    staff_options_window()
                else:
                    sg.popup_error("Login Failed", "Invalid username or password")

    db.close()
    window.close()

# Function 3: Special administrator window access only for some people
def admin_window():

    sg.theme('BrownBlue')

    layout = [
        [sg.Text("AUTHORISED ACCESS ONLY, DO NOT COMMIT ANY CHANGES WHEN NOT TOLD TO DO SO.")],
        [sg.Button('Employee Attendance'), sg.Button('Employee Info')],
        [sg.Button('Customer Orders'), sg.Button('Customer Details')],
        [sg.Exit(), sg.Button('Logout')]
    ]
    window = sg.Window('Admin Window', layout, finalize=True)

    while True:
        event, _ = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        elif event == 'Employee Attendance':
            window.hide()
            display_attendance_tab(connect_to_database())
            
        elif event == 'Employee Info':
            window.hide()
            employee_info_tab(connect_to_database())
        elif event == 'Customer Orders':
            window.hide()
            display_all_orders_admin(connect_to_database())
            
        elif event == 'Customer Details':
            window.hide()
            fetch_all_and_displaywindow_admintab(connect_to_database())
        
        elif event == 'Logout':
            window.hide()
            staff_login_window(connect_to_database())

    window.close()

def display_all_orders_admin(db):
    sg.theme('BrownBlue')
    layout = [
        [sg.Text("All Orders", font=("Helvetica", 18))],
        [sg.Table(values=[], headings=["Cust. ID", "Phone No.", "Delivery Address", "Note", "Time", "Status"], 
                  auto_size_columns=False, col_widths=[6, 13, 25, 20, 15, 13], display_row_numbers=False, 
                  justification="center", num_rows=20, key='-TABLE-')],
        [sg.Exit(), sg.Button('Back')]
    ]

    window = sg.Window("All Orders", layout, finalize=True)

    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM orders JOIN customers ON orders.Cust_PhoneNumber = customers.Cust_PhoneNumber;")
        orders = cursor.fetchall()
        table_data = []

        for order in orders:
            table_data.append([order["Cust_ID"], order["Cust_PhoneNumber"], order["Cust_HomeAddress"], order["Note"], order["Time"], order["Delivery_Status"]])

        window['-TABLE-'].update(values=table_data)

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "Exit"):
            break
        if event == 'Back':
            window.close()
            admin_window()

    window.close()

def fetch_all_and_displaywindow_admintab(db):
    try:
        cursor = db.cursor()
        cursor.execute("SELECT * from customers")
        customer_data = cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error: {err}")

    sg.theme('BrownBlue')

    layout = [
        [sg.TabGroup([
            [sg.Tab('Retrieve Customer Info', [
                [sg.Table(values=customer_data, headings=["CustID", "Name", "Gender", "Email", "Password"], auto_size_columns=True, display_row_numbers=False, justification="center", num_rows=10, key='-TABLE-')],
            ])],
            [sg.Tab('Delete Customer', [
                [sg.Text('Enter Customer ID:'), sg.InputText(key='-CUSTOMER_ID-')],
                [sg.Text('Enter Customer Name:'), sg.InputText(key='-CUSTOMER_NAME-')],
                [sg.Button('Delete'), sg.Button('Cancel')]
            ])],
            [sg.Tab('Update Customer Info', [
                [sg.Text('Enter Customer ID:'), sg.InputText(key='-CUSTOMER_ID2-')],
                [sg.Button('Submit'), sg.Button('Cancel')],
                [sg.Text(key='-CUSTOMER_INFO-')],
                [sg.Button('Change Customer Name'), sg.Button('Change Customer Gender'), sg.Button('Change Email Address'), sg.Button('Change Password')]
            ])],
        ])],
        [sg.Exit(), sg.Button('Back')]
    ]
    window = sg.Window('Customer Information', layout)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        elif event == 'Back':
            window.hide()
            admin_window()
        elif event == 'Delete':
            customer_id = values['-CUSTOMER_ID-']
            customer_name = values['-CUSTOMER_NAME-']

            if customer_id and customer_name:
                try:
                    cursor.execute('DELETE FROM customers WHERE Cust_ID=%s AND Cust_Name=%s;', (customer_id, customer_name))
                    db.commit()
                    sg.popup('Customer Deleted Successfully!')
                except mysql.connector.Error as err:
                    sg.popup_error(f"Error: {err}")
        elif event == 'Submit':
            customer_id = values['-CUSTOMER_ID2-']
            cursor.execute('SELECT * FROM customers WHERE Cust_ID=%s', (customer_id,))
            customer_info = cursor.fetchone()
            print(customer_info)

            if customer_info:
                window['-CUSTOMER_INFO-'].update(f"Customer ID: {customer_info[0]}, Customer Name: {customer_info[1]}, Gender: {customer_info[2]}\nEmail Address: {customer_info[3]}, Phone Number: {customer_info[4]}, Password: {customer_info[5]}")

        elif event == 'Change Customer Name':
            new_customer_name = sg.popup_get_text('Enter new customer name:')
            if new_customer_name:
                cursor = db.cursor()
                cursor.execute('UPDATE customers SET Cust_Name=%s WHERE Cust_ID=%s', (new_customer_name, customer_id))
                db.commit()
                sg.popup('Customer Name changed successfully!')

        # Logic for changing customer gender
        elif event == 'Change Customer Gender':
            new_customer_gender = sg.popup_get_text('Enter new customer gender:')
            if new_customer_gender:
                cursor = db.cursor()
                cursor.execute('UPDATE customers SET Cust_Gender=%s WHERE Cust_ID=%s', (new_customer_gender, customer_id))
                db.commit()
                sg.popup('Customer Gender changed successfully!')

        # Logic for changing email address
        elif event == 'Change Email Address':
            new_email_address = sg.popup_get_text('Enter new email address:')
            if new_email_address:
                cursor = db.cursor()
                cursor.execute('UPDATE customers SET Cust_EmailAddress=%s WHERE Cust_ID=%s', (new_email_address, customer_id))
                db.commit()
                sg.popup('Email Address changed successfully!')

        # Logic for changing password
        elif event == 'Change Password':
            new_password = sg.popup_get_text('Enter new password:')
            if new_password:
                cursor = db.cursor()
                cursor.execute('UPDATE customers SET Cust_Password=%s WHERE Cust_ID=%s', (new_password, customer_id))
                db.commit()
                sg.popup('Password changed successfully!')

    window.close()

def display_attendance_tab(db):

    cursor = db.cursor()

    # Fetch all data from the "attendance" table
    cursor.execute("SELECT * FROM attendance;")
    attendance_data = cursor.fetchall()

    # Define the layout for the "Attendance" tab
    layout = [
        [sg.TabGroup([
        [sg.Tab('Attendance',[
            [sg.Table(values=attendance_data, headings=['Attendance ID', 'Staff ID', 'Staff Name', 'Timestamp'], 
                      auto_size_columns=True, display_row_numbers=False, justification='center',
                      key='-ATTENDANCE_TABLE-', enable_events=True)]
        ])],
        [sg.Tab('Check Staff Attendance', [
            [sg.Text("Enter Staff ID:", font=('Courier', 16)), sg.InputText(key='-STAFF_ID-')],
            [sg.Button("Fetch Timestamps"), sg.Button("Close")],
            [sg.Output(size=(50, 10), key='-OUTPUT-')]
        ])],
    ])],
    [sg.Exit(), sg.Button('Back')]   
    ]
    
    window = sg.Window('Staff Attendance', layout)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED,'Exit'):
            break
        elif event == 'Back':
            window.hide()
            admin_window()
        elif event == 'Fetch Timestamps':
            staff_id = values['-STAFF_ID-']
            if staff_id:
                cursor.execute("SELECT Timestamp FROM attendance WHERE StaffID = %s;", (staff_id,))
                timestamps = cursor.fetchall()

                if timestamps:
                    timestamp_text = '\n'.join(str(timestamp[0]) for timestamp in timestamps)
                    window['-OUTPUT-'].update(timestamp_text)
                else:
                    window["-OUTPUT-"].update(f'No timestamps found for StaffID {staff_id}')
            else:
                sg.popup_error('Please enter Staff ID.')
    window.close()

def employee_info_tab(db):
    try:
        cursor = db.cursor()
        cursor.execute('SELECT* FROM staff;')
        staff_info = cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error: {err}")

    layout = [
        [sg.TabGroup([
            [sg.Tab('Retrieve Staff Info', [
                [sg.Table(values=staff_info, headings=["StaffID", "Name", "Post", "Gender", "Password"], auto_size_columns=False, display_row_numbers=False, justification="center", num_rows=10, key='-TABLE-')],  
            ])],
            [sg.Tab('Enter New Staff Info', [
                [sg.Text("Staff ID:", font=('Courier', 16)), sg.InputText(key='-STAFF_ID-')],
                [sg.Text("Staff Name:", font=('Courier', 16)), sg.InputText(key='-STAFF_NAME-')],
                [sg.Text("Staff Post:", font=('Courier', 16)), sg.InputText(key='-STAFF_POST-')],
                [sg.Text("Gender:", font=('Courier', 16)), sg.InputText(key='-GENDER-')],
                [sg.Text("Password:", font=('Courier', 16)), sg.InputText(key='-PASSWORD-', password_char='*')],
                [sg.Button("Submit Now")],
            ])],
            [sg.Tab('Delete Staff Info', [
                [sg.Text('Enter Staff ID:'), sg.InputText(key='-ID-')],
                [sg.Text('Enter Staff Name:'), sg.InputText(key='-NAME-')],
                [sg.Button('Submit'), sg.Button('Cancel')]
            ])],
            [sg.Tab('Update Staff Info', [
                    [sg.Text('Enter Staff ID:'), sg.InputText(key='-STAFF_ID2-')],
                    [sg.Button('Submit now'), sg.Button('Cancel')],
                    [sg.Text(key='-STAFF_INFO-')],
                    [sg.Button('Change Staff Name'), sg.Button('Change Staff Post'), sg.Button('Change Gender'), sg.Button('Change Password')]
            ])]
        ])],
        [sg.Exit(), sg.Button('Back')]
    ]
    
    window = sg.Window('Employees', layout)
    while True:
        event, values = window.read()
        
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        elif event == 'Back':
            window.hide()
            admin_window()
        elif event == 'Submit':
            window.hide()
            cid = values['-ID-']
            name = values['-NAME-']
            if cid==1 and name=='Akhil Tyagi':
                sg.popup('You cant delete that bro.')
                window.close()
                break
            elif not cid==1 and not name=='Akhil Tyagi':
                try:
                    cursor = db.cursor()
                    insert_query = 'DELETE FROM staff WHERE Staff_ID=%s and Staff_Name=%s;'
                    values = (cid, name)
                    cursor.execute(insert_query, values)
                    db.commit()
                    sg.popup('Successful')
                except mysql.connector.Error as err:
                    print(f"Error: {err}")
        elif event == 'Submit Now':
            staff_id = values['-STAFF_ID-']
            staff_name = values['-STAFF_NAME-']
            staff_post = values['-STAFF_POST-']
            gender = values['-GENDER-']
            password = values['-PASSWORD-']

            if staff_id and staff_name and staff_post and gender and password:
                try:
                    insert_query2 = "INSERT INTO staff (Staff_ID, Staff_Name, Staff_Post, Gender, Password) VALUES (%s, %s, %s, %s, %s);"
                    values2 = (staff_id, staff_name, staff_post, gender, password)
                    cursor.execute(insert_query2, values2)
                    db.commit()
                    sg.popup('Staff Added Successfully!')
                except mysql.connector.Error as err:
                    sg.popup_error(f"Error: {err}")
            else:
                sg.popup_error("Please fill in all fields.")
        elif event == 'Submit now':
            staff_id2 = values['-STAFF_ID2-']
            cursor.execute('SELECT * FROM staff WHERE Staff_ID=%s', (staff_id2,))
            staff_info = cursor.fetchone()
            

            if staff_info:
                window['-STAFF_INFO-'].update(f"Staff ID: {staff_info[0]}, Staff Name: {staff_info[1]}, Staff Post: {staff_info[2]}\nGender: {staff_info[3]}, Password: {staff_info[4]}")

        elif event == 'Change Staff Name':
            new_staff_name = sg.popup_get_text('Enter new staff name:')
            if new_staff_name:
                cursor.execute('UPDATE staff SET Staff_Name=%s WHERE Staff_ID=%s', (new_staff_name, staff_id2))
                db.commit()
                sg.popup('Staff Name changed successfully!')

        # Logic for changing staff post
        elif event == 'Change Staff Post':
            new_staff_post = sg.popup_get_text('Enter new staff post:')
            if new_staff_post:
                cursor = db.cursor()
                cursor.execute('UPDATE staff SET Staff_Post=%s WHERE Staff_ID=%s', (new_staff_post, staff_id2))
                db.commit()
                sg.popup('Staff Post changed successfully!')

        # Logic for changing gender
        elif event == 'Change Gender':
            new_gender = sg.popup_get_text('Enter new gender:')
            if new_gender:
                cursor = db.cursor()
                cursor.execute('UPDATE staff SET Gender=%s WHERE Staff_ID=%s', (new_gender, staff_id2))
                db.commit()
                sg.popup('Gender changed successfully!')

        # Logic for changing password
        elif event == 'Change Password':
            new_password = sg.popup_get_text('Enter new password:')
            if new_password:
                cursor = db.cursor()
                cursor.execute('UPDATE staff SET Password=%s WHERE Staff_ID=%s', (new_password, staff_id2))
                db.commit()
                sg.popup('Password changed successfully!')
     
    window.close()

def staff_info_window(db):
    sg.theme('LightGrey1')  # Set the theme
    window = sg.Window('Staff Information', [
        [sg.Text('Enter Staff ID:'), sg.InputText(key='-STAFF_ID-')],
        [sg.Button('Submit'), sg.Button('Cancel')]
    ])

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'Cancel':
            break
        elif event == 'Submit':
            staff_id = values['-STAFF_ID-']
            cursor = db.cursor()
            cursor.execute('SELECT FROM staff WHERE Staff_ID=%s',(staff_id,))
            staff_info = cursor.fetchone()

            if staff_info:
                info_window = sg.Window('Staff Information', [
                    [sg.Text(f"Staff ID: {staff_info['staff_id']}")],
                    [sg.Text(f"Staff Name: {staff_info['staff_name']}")],
                    [sg.Text(f"Staff Post: {staff_info['staff_post']}")],
                    [sg.Text(f"Gender: {staff_info['gender']}")],
                    [sg.Text(f"Password: {staff_info['password']}")],
                    [sg.Button('Change Staff Name'), sg.Button('Change Staff Post'), sg.Button('Change Gender'), sg.Button('Change Password'), sg.Button('Cancel')]
                ])

                while True:
                    event, values = info_window.read()

                    if event == sg.WIN_CLOSED or event == 'Cancel':
                        info_window.close()
                        break
                    elif event == 'Change Staff Name':
                        new_staff_name = sg.popup_get_text('Enter new staff name:')
                        if new_staff_name:
                            # Update the staff name in the database and refresh the display
                            staff_info['staff_name'] = new_staff_name
                            info_window['-STAFF_NAME-'].update(f"Staff Name: {staff_info['staff_name']}")
                    # Similar logic for other fields (Staff Post, Gender, Password) goes here

                info_window.close()

    window.close()
    
# Function 4: Once the staff logins asking them what they want to do
def staff_options_window():

    sg.theme('BrownBlue')
    layout = [
        [sg.Text("Staff Options", font=("Helvetica", 18))],
        [sg.Text("What do you want to do now? @-@")],
        [sg.Button("Customer Orders"), sg.Button('Customer Details')],
        [sg.Button("Products"), sg.Button('Categories')],
        [sg.Exit(), sg.Button('Logout')]
    ]
    window = sg.Window("Staff Options", layout, finalize=True)

    while True:
        event, _ = window.read()
        if event in ('Customer Orders','Customer Details','Products','Categories'):
            window.hide()
        if event == sg.WIN_CLOSED or event == "Exit":
            break
        if event == 'Logout':
            window.hide()
            staff_login_window(connect_to_database())
        elif event == "Customer Orders":
            display_all_orderstab(connect_to_database())
        elif event == "Customer Details":
            fetch_all_and_displaywindowtab(connect_to_database())
        elif event == "Products":
            # Call a function to add a new product
            add_product_to_dbtab(connect_to_database())
        elif event == "Categories":
            # Call a function to add a new category
            add_category_to_dbtab(connect_to_database())
    
    window.close()

# Function 5: To display all the orders
def display_all_orderstab(db):
    sg.theme('BrownBlue')
    layout = [
        [sg.TabGroup([
            [sg.Tab('Display Orders', [
                [sg.Text("All Orders", font=("Helvetica", 18))],
                [sg.Table(values=[], headings=["Cust. ID", "OrderID", "Phone No.", "Delivery Address", "Note", "Time", "Status"], 
                        auto_size_columns=False, col_widths=[6, 8, 13, 25, 20, 15, 13], display_row_numbers=False, justification="center", num_rows=20, key='-TABLE-')]
            ])],
            [sg.Tab('Update Orders', [
                [sg.Text('Enter Order ID:'), sg.InputText(key='-ORDER_ID-')],
                [sg.Text('Select Delivery Status:'), sg.Radio('Delivered', group_id='-DELIVERY_STATUS-', key='-DELIVERED-', default=False), sg.Radio('Not Delivered', group_id='-DELIVERY_STATUS-', key='-NOT_DELIVERED-', default=False)],
                [sg.Button('Update'), sg.Button('Cancel')]
            ])],
        ])],
        [sg.Exit(), sg.Button('Back')]
    ]
    window = sg.Window('Customer Orders', layout, finalize=True)

    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM orders JOIN customers ON orders.Cust_PhoneNumber = customers.Cust_PhoneNumber;")
        orders = cursor.fetchall()
        table_data = []

        for order in orders:
            table_data.append([order["Cust_ID"], order["OrderID"], order["Cust_PhoneNumber"], order["Cust_HomeAddress"], order["Note"], order["Time"], order["Delivery_Status"]])

        window['-TABLE-'].update(values=table_data)

    except mysql.connector.Error as err:
        print(f"Error: {err}")


    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        elif event == 'Back':
            window.hide()
            staff_options_window()
        elif event == 'Update':
            order_id = values['-ORDER_ID-']
            delivered = values['-DELIVERED-']
            
            if order_id:
                try:
                    delivery_status = 'Delivered' if delivered else 'Not Delivered'
                    cursor.execute('UPDATE orders SET Delivery_Status=%s WHERE OrderID=%s;', (delivery_status, order_id))
                    db.commit()
                    sg.popup('Delivery Status Updated Successfully!')
                except mysql.connector.Error as err:
                    sg.popup_error(f"Error: {err}")
    window.close()


# Function 6: To fetch all from the table customers and display it in a window see_customer_data
def fetch_all_and_displaywindowtab(db):
    try:
        cursor = db.cursor()
        cursor.execute("SELECT * from customers")
        customer_data = cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error: {err}")

    sg.theme('BrownBlue')

    layout = [
        [sg.Text("Customer Details", font=("Helvetica", 18))],
        [sg.Table(values=customer_data, headings=["CustID", "Name", "Gender", "Email", "Password"], auto_size_columns=True,
                  display_row_numbers=False, justification="center", num_rows=10, key='-TABLE-')],
        [sg.Exit(), sg.Button('Back')]
    ]

    window = sg.Window("Customer Details", layout, finalize=True)
    while True:
        event, _ = window.read()
        if event in (sg.WIN_CLOSED, "Exit"):
            break
        if event == 'Back':
            window.hide()
            staff_options_window()

    window.close()

# Function 7: To take inputs from the staff for the new product and then insert the values into the products table
def add_product_to_dbtab(db):
    layout = [
        [sg.TabGroup([
            [sg.Tab('Add Product', [
                [sg.Text("Add New Product", font=("Helvetica", 18))],
                [sg.Text("Product Name:"), sg.InputText(key='-PRODUCTNAME-')],
                [sg.Text("Price:"), sg.InputText(key='-PRICE-')],
                [sg.Text("Category ID:"), sg.InputText(key='-CATEGORYID-')],
                [sg.Button("Add Product", bind_return_key=True)]
            ])],
            [sg.Tab('Delete Product', [
                [sg.Text('Enter Product ID:'), sg.InputText(key='-PRODUCT_ID-')],
                [sg.Text('Enter Product Name:'), sg.InputText(key='-PRODUCT_NAME-')],
                [sg.Button('Delete'), sg.Button('Cancel')]
            ])],
        ])],
        [sg.Exit(), sg.Button('Back')]
    ]
    window = sg.Window('Products', layout)
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        elif event == 'Back':
            window.hide()
            
        elif event == 'Add Product':
            window.hide()
            product_name = values['-PRODUCTNAME-']
            price = values['-PRICE-']
            category_id = values['-CATEGORYID-']
            try:
                cursor = db.cursor()
                insert_query = "INSERT INTO products (ProductName, Price, CategoryID) VALUES (%s, %s, %s);"
                values = (product_name, price, category_id)
                cursor.execute(insert_query, values)
                db.commit()
                sg.popup(f"Task completed successfully!\n{product_name} was successfully added as a product in the system!")
                staff_options_window()

            except mysql.connector.Error as err:
                sg.popup_error(f"Error occurred during product addition: {err}")
        elif event == 'Delete':
            product_id = values['-PRODUCT_ID-']
            product_name = values['-PRODUCT_NAME-']

            if product_id and product_name:
                try:
                    cursor = db.cursor()
                    cursor.execute('DELETE FROM products WHERE ProductID=%s AND ProductName=%s;', (product_id, product_name))
                    db.commit()
                    sg.popup('Product Deleted Successfully!')
                except mysql.connector.Error as err:
                    sg.popup_error(f"Error: {err}")
    window.close()

# Function 8: To take inputs from the staff for the new category and then insert the values into the table categories
def add_category_to_dbtab(db):
    layout=[
        [sg.TabGroup([
            [sg.Tab('Create Category', [
                [sg.Text("Add New Category", font=("Helvetica", 18))],
                [sg.Text("Category ID:"), sg.InputText(key='-CATEGORYID-')],
                [sg.Text("Category Name:"), sg.InputText(key='-CATEGORYNAME-')],
                [sg.Text("\nCategoryID should not be matching with any existing ones.")],
                [sg.Button("Add Category", bind_return_key=True)]
        ])],
        [sg.Tab('Delete Category', [
            [sg.Text('Enter Category ID:'), sg.InputText(key='-CATEGORY_ID-')],
            [sg.Text('Enter Category Name:'), sg.InputText(key='-CATEGORY_NAME-')],
            [sg.Text("\nNo Product should be existing in the deleting category.")],
            [sg.Button('Delete'), sg.Button('Cancel')]
        ])],
    ])],
    [sg.Exit(), sg.Button('Back')]
]
    window = sg.Window('Categories', layout)
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        elif event == 'Back':
            window.hide()
            staff_options_window()
        elif event == 'Add Category':
            window.hide()
            category_id = values['-CATEGORYID-']
            category_name = values['-CATEGORYNAME-']
            try:
                cursor = db.cursor()
                insert_query = "INSERT INTO categories (CategoryID, CategoryName) VALUES (%s, %s);"
                values = (category_id, category_name)
                cursor.execute(insert_query, values)
                db.commit()
                sg.popup(f"Task completed successfully!\n{category_name} with categoryid:{category_id} was  added as a product in the system!")
                staff_options_window()

            except mysql.connector.Error as err:
                sg.popup_error(f"Error occurred during category addition: {err}")
        elif event == 'Delete':
            category_id = values['-CATEGORY_ID-']
            category_name = values['-CATEGORY_NAME-']

            if category_id and category_name:
                try:
                    cursor = db.cursor()
                    cursor.execute('DELETE FROM categories WHERE CategoryID=%s AND CategoryName=%s;', (category_id, category_name))
                    db.commit()
                    sg.popup('Category Deleted Successfully!')
                except mysql.connector.Error as err:
                    sg.popup_error(f"Error: {err}")

# Function 9: Create a customer registration window
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

            if db:
                if insert_customer_data(db, name, gender, email, phone, password):
                    sg.popup(f"Welcome {name}! \n\nYour account has been successfully created with the login details you have provided.\nPlease login to your account using your Phone Number and Password. \n\n(You will be redirected to the main page when you click OK)")
                    customer_phone = phone
                    window.close()
                    main()

                else:
                    sg.popup_error("Error occurred during registration. Please try again later.")

                db.close()

        elif event == 'Back':
            window.hide()
            main()
        
        window.close()

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

# Function 11: Create a login window for customers
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
                sg.popup("Login Successful", f"Welcome, {user[1]}. Have a lovely day :D \n\n{f}")
                
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

# Function 12: Create a customer order window
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

# Function 13: Create a window for order creation
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

# Function 17: To create the billing window
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

# Function 18: To take inputs from the user about their order and inserts it into table orders
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
                sg.popup(f"Order successfully created! \nWill be delivered at {address}.\n\n{f}")
                customer_order_window(db)
            except mysql.connector.Error as err:
                print(f"Error: {err}")

        elif event == 'Cancel':
            window.hide()
            customer_order_window(db)
            
            window.close()
            break

    window.close()

# Function 19: To display the customers order info if they select see existing orders, in a window ask for their phone number and then retrieve data from database
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

# Function 20: Main function
def main():
    sg.theme('BrownBlue')

    # Create a window for user type selection
    layout_choice = [
        [sg.Image(filename="meow.png")],
        [sg.Text("Welcome to da cool store", font=('Courier', 20))],
        [sg.Text("Are you a staff member or a customer?", font=('Arial', 15))],
        [sg.Button("Staff"), sg.Button("New User"), sg.Button("Existing User"), sg.Exit()]
    ]

    window_choice = sg.Window('Da Cool Store', layout_choice, element_justification="c", size=(500, 450))

    while True:
        event_choice, _ = window_choice.read()

        if event_choice in ('Staff','New User','Existing User'):
            window_choice.close()

        if event_choice == sg.WIN_CLOSED or event_choice == "Exit":
            break
        elif event_choice == "Staff":
            staff_login_window(connect_to_database())
        elif event_choice == "New User":
            window_choice.close()  # Close the current window
            customer_registration_window()
        elif event_choice == "Existing User":
            window_choice.close()  # Close the current window
            customer_login_window(connect_to_database())    

    window_choice.close()

import PySimpleGUI as sg
import database

def staff_login_window(db):
    sg.theme('BrownBlue')
    layout = [
        [sg.Text("Staff ID:", font=('Courier', 20)), sg.InputText(key='-ID-')],
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
            from utils import main
            main()
        elif event == 'Login':
            window.hide()
            cid = values['-ID-']
            password = values['-PASSWORD-']

            # Staff validation logic here
            if cid == '1' and password in ('akhil1202','a','1202'):
                sg.popup('Admin functionality acquired. Please use with care.')
                from admin import admin_window
                admin_window()
                break
            else:
                cursor.execute("SELECT * FROM staff WHERE Staff_ID=%s AND Password=%s;", (cid, password))
                user = cursor.fetchone()

                if user:
                    sg.popup("Login Successful! Welcome, {user[1]}.")
                    window.close()
                    staff_options_window()
                else:
                    sg.popup_error("Login Failed", "Invalid username or password")

    db.close()
    window.close()

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

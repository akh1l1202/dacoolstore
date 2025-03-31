import PySimpleGUI as sg
from database import connect_to_database
import mysql.connector

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
            from staff import staff_login_window
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

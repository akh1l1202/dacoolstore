import PySimpleGUI as sg

# Function to display the billing window
def billing_window(order_details):
    sg.theme('DarkBlue')
    order_details = fetch_order_details(db)

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
        category_name = order["categoryname"]
        product_name = order["productname"]
        product_price = order["productprice"]
        total_amount += product_price

        table_data.append([serial_number, category_name, product_name, f"${product_price:.2f}"])
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

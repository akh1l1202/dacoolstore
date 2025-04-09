import PySimpleGUI as sg
from database import connect_to_database, check_and_create_tables, insert_sample_data
from staff import staff_login_window


def main():
    insert_sample_data()
    sg.theme('BrownBlue')

    layout_choice = [
        [sg.Image(filename="meow.png")],
        [sg.Text("Welcome to Da Cool Store", font=('Courier', 20))],
        [sg.Text("Are you a staff member or a customer?", font=('Arial', 15))],
        [sg.Button("Staff"), sg.Button("New User"), sg.Button("Existing User"), sg.Exit()]
    ]

    window_choice = sg.Window('Da Cool Store', layout_choice, element_justification="c", size=(500, 450))

    while True:
        event_choice, _ = window_choice.read()

        if event_choice in ('Staff', 'New User', 'Existing User'):
            window_choice.close()
        
        if event_choice == sg.WIN_CLOSED or event_choice == "Exit":
            break
        elif event_choice == "Staff":
            staff_login_window(connect_to_database())
        elif event_choice == "New User":
            from customer import customer_registration_window
            customer_registration_window()
        elif event_choice == "Existing User":
            from customer import customer_login_window
            customer_login_window(connect_to_database())

    window_choice.close()

if __name__ == "__main__":

    # Check and create tables before anything else
    check_and_create_tables()
    
    main()

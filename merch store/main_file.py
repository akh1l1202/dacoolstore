import PySimpleGUI as sg
from functions import *

def main():
    sg.theme('DarkBlue')

    # Create a window for user type selection
    layout_choice = [
        [sg.Text("Are you a staff member or a customer?")],
        [sg.Button("Staff"), sg.Button("New User"), sg.Button("Existing User"), sg.Exit()]
    ]

    window_choice = sg.Window('User Type', layout_choice)

    while True:
        event_choice, _ = window_choice.read()

        if event_choice == sg.WIN_CLOSED or event_choice == "Exit":
            break
        elif event_choice == "Staff":
            window_choice.close()
            staff_login_window(connect_to_database())
        elif event_choice == "New User":
            window_choice.close()  # Close the current window
            customer_registration_window()
        elif event_choice == "Existing User":
            window_choice.close()  # Close the current window
            customer_login_window(connect_to_database())

    window_choice.close()

# Create a window to display billing window


if __name__ == "__main__":
    main()

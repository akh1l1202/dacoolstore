import PySimpleGUI as sg
from functions import *

# Main function
def main():
    sg.theme('BrownBlue')

    # Create a window for user type selection
    layout_choice = [
        [sg.Image(filename="meow.png")],
        [sg.Text("Welcome to da cool store", font=('Courier', 20))],
        [sg.Text("Are you a staff member or a customer?", font=('Arial', 15))],
        [sg.Button("Staff"), sg.Button("New User"), sg.Button("Existing User"), sg.Exit()]
    ]

    window_choice = sg.Window('Da Cool Store', layout_choice, element_justification="c")

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

if __name__ == "__main__":
    main()

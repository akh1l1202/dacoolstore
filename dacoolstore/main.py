import os

import PySimpleGUI as sg

from dacoolstore.database import connect_to_database, insert_sample_data


def make_main_window():
    """Create and return the main choice window."""
    sg.theme("BrownBlue")

    # Dynamically locate the assets folder relative to this file
    assets_dir = os.path.join(os.path.dirname(__file__), "assets")
    image_path = os.path.join(assets_dir, "meow.png")

    layout_choice = [
        [sg.Image(filename=image_path) if os.path.exists(image_path) else sg.Text("[Store Logo]")],
        [sg.Text("Welcome to Da Cool Store", font=("Courier", 20))],
        [sg.Text("Are you a staff member or a customer?", font=("Arial", 15))],
        [sg.Button("Staff"), sg.Button("New User"), sg.Button("Existing User"), sg.Exit()],
    ]

    return sg.Window("Da Cool Store", layout_choice, element_justification="c", size=(500, 450))


def main():
    """Main application loop managing top-level GUI transitions."""
    # Ensure sample data is present
    insert_sample_data()

    while True:
        window_choice = make_main_window()
        event_choice, _ = window_choice.read()
        window_choice.close()

        if event_choice in (sg.WIN_CLOSED, "Exit"):
            break

        # Establish database connection for the sub-windows
        db = connect_to_database()
        if not db:
            sg.popup_error("Database Connection Failed", "Please check your database server and config.")
            continue

        try:
            if event_choice == "Staff":
                from dacoolstore.staff import staff_login_window

                if staff_login_window(db) == "EXIT":
                    break
            elif event_choice == "New User":
                from dacoolstore.customer import customer_registration_window

                if customer_registration_window(db) == "EXIT":
                    break
            elif event_choice == "Existing User":
                from dacoolstore.customer import customer_login_window

                if customer_login_window(db) == "EXIT":
                    break
        finally:
            if db:
                db.close()


if __name__ == "__main__":
    from dacoolstore.database import check_and_create_tables

    # Check and create tables before running the app
    check_and_create_tables()
    main()

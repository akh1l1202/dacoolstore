1. *GUI Development:*

   - Create a main window with login functionality for both customers and staff.
   - After successful login, show options for customers and staff.

2. *Customer Functionality:*

   - After customer login, show options to "See My Orders" and "Make an Order."
   - Implement logic to display existing orders and allow customers to view their order details from the `OrderItems` table.
   - Implement logic to allow customers to browse categories, select products, and place new orders.
   - Display billing window after placing an order and input the order info the the `Orders` table.

3. *Staff Functionality:*

   - Implement staff login functionality and display staff-specific options.
   - Provide access to customer information and order details for staff.
   - Allow staff to add new categories and products, which will involve inserting data into the `Categories` and `Products` tables.

4. *Database Interaction:*

   - Implement functions to interact with the database, including retrieving customer information, orders, products, and categories, as well as inserting new data.

5. *User Authentication:*

   - Implement secure user authentication for both customers and staff.
   - Hash and store passwords securely in the database.

6. *Category and Product Display:*

   - Retrieve categories and products from the database and display them on the GUI.
   - Allow customers to select products and add them to their orders.

7. *Order Processing:*

   - Implement the logic for customers to place orders, including inserting order information into the `Orders` and `OrderItems` tables.

8. *GUI Navigation:*

   - Implement buttons and navigation to transition between different screens and functionalities based on user choices.

9. *Error Handling and Validation:*

   - Implement validation to ensure correct inputs and handle potential errors.

10. *Testing:*

    - Thoroughly test your application to ensure all features work as intended.

11. *Deployment and Iteration:*

    - Deploy your application and gather user feedback.
    - Iterate and improve based on feedback, adding new features and refining existing ones.

12. *All functions:*

    - Function 1: Establishes a connection to the MySQL database
    - Function 2: Creates a login window for staff, verifies the userid and password.
    - Function 3: Special administrator window access only for some people
    - Function 4: Asks the staff person, what they want to do now.
    - Function 5: Displays all orders made by the customers to the staff.
    - Function 6: Displays all info of the customers to the staff.
    - Function 7: Adds products.
    - Function 8: Adds categories.
    - Function 9: Creates a customer registration window and takes all their information.
    - Function 10: Stores the customer data into the table.
    - Function 11: Creates a login window, and verifies the customer phone number and password.
    - Function 12: Creates a customer order window and asks them what they want to do.
    - Function 13: Creates a window for order creation.
    - Function 14: Fetches categories from the table.
    - Function 15: Fetches products by categories from the table.
    - Function 16: Fetches information of the products selected by the customer in order creation.
    - Function 17: Creates a billing window and totals the amount.
    - Function 18: Takes inputs from the user about their order.
    - Function 19: Displays the customers order info if the customer selects see existing orders, asks for their phone number and then retrieves data.
    - Function 20: Main function, displaying the main gui window.

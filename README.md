## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
![License](https://img.shields.io/badge/license-MIT-blue.svg)


# Da Cool Store

Welcome to **Da Cool Store**! This is an online store application built using Python and PySimpleGUI that allows customers and staff to interact seamlessly. Customers can register, log in, and browse products, while staff members have access to their own login system to manage the store.

## Features

- **Staff Login**: Secure login system for staff members with role-based access.
- **Customer Registration & Login**: Customers can create new accounts or log into their existing ones.
- **Product Management**: Staff can add, update, and manage products available in the store.
- **Order Management**: Customers can place orders and track their delivery status.
- **Database Integration**: The app integrates with a MySQL database to store customer and staff information, orders, and products.

## Technologies Used

- **Python**: The main programming language used for the application.
- **PySimpleGUI**: A simple and easy-to-use graphical user interface (GUI) library for building desktop applications.
- **MySQL**: A relational database management system to store all store-related data, including staff, customers, and orders.
- **MySQL Connector for Python**: A Python library used to connect and interact with MySQL databases.

## Installation

Follow the steps below to get the application running on your local machine:

### 1. Clone the repository:

```bash
git clone https://github.com/your-username/da-cool-store.git
cd da-cool-store
```
2. Create a virtual environment (optional but recommended):
```bash

python -m venv venv
```
3. Activate the virtual environment:
For Windows:

```bash
venv\Scripts\activate
```
For Mac/Linux:

```bash
source venv/bin/activate
```
4. Install required dependencies:
```bash
pip install -r requirements.txt
```
5. Set up the database:
Install MySQL if you haven't already, and set up a database named dacoolstore.

Import the SQL dump file provided in the database folder into your MySQL instance to create all the necessary tables.

```bash
mysql -u root -p dacoolstore < database/dacoolstore.sql
```
6. Configure the database connection:
Open database.py and ensure that the MySQL database credentials (host, user, password) are correctly set for your local MySQL instance.

7. Run the application:
```bash
python utils.py
```
This will launch the application. Follow the on-screen prompts to interact with the store.

Screenshots
Welcome Screen
Staff Login
Customer Registration

Contributing
We welcome contributions to Da Cool Store! To contribute:

Fork this repository.
Create a new branch (git checkout -b feature/your-feature).
Make your changes.
Commit your changes (git commit -m 'Add new feature').
Push to the branch (git push origin feature/your-feature).
Open a pull request.

License
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgments
PySimpleGUI: For the easy-to-use GUI framework.
MySQL: For the database management system.
OpenAI: For their AI models used to assist in code development.

Contact
If you have any questions or feedback, feel free to reach out to the project maintainers:
Email: tyagi.akhil1202@gmail.com
GitHub: https://github.com/akh1l1202

Happy coding! 🎉

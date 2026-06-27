from unittest import mock

from dacoolstore.database import fetch_categories, fetch_products_by_category, table_exists


def test_table_exists():
    # Verify table_exists execution logic
    mock_cursor = mock.Mock()

    # Case: Table exists
    mock_cursor.fetchone.return_value = ("categories",)
    assert table_exists(mock_cursor, "categories") is True
    mock_cursor.execute.assert_called_with("SHOW TABLES LIKE %s", ("categories",))

    # Case: Table does not exist
    mock_cursor.fetchone.return_value = None
    assert table_exists(mock_cursor, "orders") is False


def test_fetch_categories():
    # Verify fetch_categories returns unique category names
    mock_db = mock.Mock()
    mock_cursor = mock_db.cursor.return_value
    mock_cursor.fetchall.return_value = [("Groceries",), ("Books",), ("Clothing",)]

    categories = fetch_categories(mock_db)
    assert categories == ["Groceries", "Books", "Clothing"]
    mock_cursor.execute.assert_called_with("SELECT DISTINCT CategoryName FROM categories;")
    mock_cursor.close.assert_called_once()


def test_fetch_products_by_category():
    # Verify fetch_products_by_category queries database and maps results properly
    mock_db = mock.Mock()
    mock_cursor = mock_db.cursor.return_value
    mock_cursor.fetchall.return_value = [("Eggs",), ("Milk",)]

    products = fetch_products_by_category(mock_db, "Groceries")
    assert products == ["Eggs", "Milk"]
    mock_cursor.close.assert_called_once()

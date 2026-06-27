from dacoolstore.database import check_and_create_tables
from dacoolstore.main import main

if __name__ == "__main__":
    check_and_create_tables()
    main()

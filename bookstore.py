# Import the necessary modules.
import sqlite3
from tabulate import tabulate


# Define a function to create the table named "books".
def create_table():
    cursor.execute("""CREATE TABLE books(
        Id TEXT PRIMARY KEY,
        Title TEXT,
        Author TEXT,
        Quantity INTEGER)
        """)
    db.commit()


# Define a function to get the table "books" length.
def table_count():
    cursor.execute("SELECT * FROM books")
    count = len(cursor.fetchall())
    return count


# Define a function to insert into the table "books" the data stored in the
# variable list "book_list".
def populate_table():
    # Create a list that stores few books.
    book_list = [(3001, "A Tale of Two Cities", "Charles Dickens", 30),
                 (3002, "Harry Potter and the Philosopher's Stone",
                  "J.K. Rowling", 40),
                 (3003, "The Lion, the Witch and the Wardrobe",
                  "C.S. Lewis", 25),
                 (3004, "The Lord of the Rings", "J.J.R. Tolkien", 37),
                 (3005, "Alice in Wonderland", "Lewis Carroll", 12)]

    cursor.executemany("""INSERT INTO books
            VALUES(?,?,?,?)""", book_list)
    db.commit()


# Define a function to display all books stored inside the table.
def display_books():
    if table_count() > 0:
        table = [["ID", "TITLE", "AUTHOR", "QUANTITY"]]
        cursor.execute("""SELECT * FROM books""")
        for row in cursor:
            table.append([row[0], row[1], row[2], row[3]])
        print("\nLIST OF BOOKS")
        print(tabulate(table, headers='firstrow', tablefmt='fancy_grid',
                       numalign="center", stralign="center"))
        print("YOU CAN FIND ABOVE THE LIST OF BOOKS.")
    else:
        print("\nWe are sorry, there are not books at the moment, you can "
              "add them selecting the option 2 from the menu.")


# Define a function to create and add new books into the table "books".
def insert_book():
    print("\nINSERT BOOK")
    while True:
        book_id = input("Enter the book ID: ").strip()
        cursor.execute("""SELECT * FROM books WHERE upper(Id) = ?""",
                       ((book_id.upper()),))
        if cursor.fetchone() is not None:
            print("We are sorry the entered ID already exists, please enter a "
                  "different one.")
        else:
            break
    book_title = input("Enter the book title: ").strip()
    book_author = input("Enter the book author: ").strip()
    while True:
        try:
            book_qty = int(input("Enter the book quantity: "))
            break
        except ValueError:
            print("We are sorry, you entered a wrong input, please try again.")

    cursor.execute("""INSERT INTO books
                    VALUES(?,?,?,?)""", (book_id, book_title, book_author,
                                         book_qty))
    db.commit()
    print("\nThe book has been added.")


# Define a function to update the existing books based on one of the following
# parameters ID/title/author/quantity.
def update_book():
    if table_count() > 0:
        print("\nUPDATE BOOK")
        book_data = input("Enter the ID or the title of the book that you "
                          "want to update: ").upper().strip()
        cursor.execute("""SELECT * FROM books WHERE upper(Id) = ? 
        OR upper(Title) = ?""", (book_data, book_data))
        if cursor.fetchone() is not None:
            while True:
                data_to_change = input("""\nWhich data do you want to update?
1 - ID
2 - Title
3 - Author
4 - Quantity
0 - Go back to the menu
Enter the number of your choice: """)
                if data_to_change == "1":
                    book_id = input("Enter the new ID: ").strip()
                    cursor.execute("""SELECT * FROM books WHERE upper(Id) = 
                    ?""", ((book_id.upper()),))
                    if cursor.fetchone() is not None:
                        print("\nWe are sorry the entered ID already exists, "
                              "please enter a different one.")
                    else:
                        cursor.execute("""UPDATE books SET Id = ? WHERE 
                        upper(Id) =  ? OR upper(Title) = ?""",
                                       (book_id, book_data, book_data))
                        db.commit()
                        print("\nThe book has been updated.")
                        break
                elif data_to_change == "2":
                    book_title = input("Enter the new title: ").strip()
                    cursor.execute("""UPDATE books SET Title = ? WHERE 
                    upper(Id) = ? OR upper(Title) = ?""",
                                   (book_title, book_data, book_data))
                    db.commit()
                    print("\nThe book has been updated.")
                    break
                elif data_to_change == "3":
                    book_author = input("Enter the new author: ").strip()
                    cursor.execute("""UPDATE books SET Author = ? WHERE 
                    upper(Id) = ? OR upper(Title) = ?""",
                                   (book_author, book_data, book_data))
                    db.commit()
                    print("\nThe book has been updated.")
                    break
                elif data_to_change == "4":
                    try:
                        book_qty = int(input("Enter the new quantity: "))
                        cursor.execute("""UPDATE books SET Quantity = ? 
                        WHERE upper(Id) = ? OR upper(Title) = ?""",
                                       (book_qty, book_data, book_data))
                        db.commit()
                        print("\nThe book has been updated.")
                        break
                    except ValueError:
                        print("\nWe are sorry, you entered a wrong "
                              "input, please try again and be sure to "
                              "enter a number.")
                elif data_to_change == "0":
                    break
                else:
                    print("\nWe are sorry, you entered a wrong "
                          "choice, please try again.")

        else:
            print("\nWe are sorry, we didn't find any book with this data, "
                  "please try again.")
    else:
        print("\nWe are sorry, there are not books at the moment, you can "
              "add them selecting the option 2 from the menu.")


# Define a function to delete specific books.
def delete_book():
    if table_count() > 0:
        print("\nDELETE BOOK")
        book_data = input("Enter the ID or the title of the book to delete: "
                          "").upper().strip()
        cursor.execute("""SELECT * FROM books WHERE upper(Id) = ? OR upper(
        Title) =  ?""", (book_data, book_data))
        if cursor.fetchone() is not None:
            cursor.execute("""DELETE FROM books WHERE upper(Id) = ? OR 
            upper(Title) = ?""", (book_data, book_data))
            db.commit()
            print("\nThe book has been deleted.")
        else:
            print("\nWe are sorry, we didn't find any book with this data, "
                  "please try again.")
    else:
        print("\nWe are sorry, there are not books at the moment, you can "
              "add them selecting the option 2 from the menu.")


# Define a function that searches for books and displays them. The research
# can be made base on one of the four parameters ID/title/author/quantity
# and the result will store every book containing that parameter.
def search_books():
    if table_count() > 0:
        print("\nSEARCH BOOK/S")
        book_data = input("Enter one between book ID/title/author/quantity: "
                          "").upper().strip()
        table = [["ID", "TITLE", "AUTHOR", "QUANTITY"]]
        cursor.execute("""SELECT * FROM books WHERE upper(Id) = ? 
        OR upper(Title) = ? OR upper(Author) = ? OR 
        quantity = ?""", (book_data, book_data, book_data, book_data))
        for row in cursor:
            table.append([row[0], row[1], row[2], row[3]])
        if len(table) > 1:
            print("\nSEARCH RESULT")
            print(tabulate(table, headers='firstrow', tablefmt='fancy_grid',
                           numalign="center", stralign="center"))
            print("YOU CAN FIND ABOVE THE SEARCH RESULT.")
        else:
            print("\nWe are sorry, we didn't find any book with this data, "
                  "please try again.")
    else:
        print("\nWe are sorry, there are not books at the moment, you can "
              "add them selecting the option 2 from the menu.")


# Define a function to delete all books from the table "books".
def delete_all():
    if table_count() > 0:
        print("\nDELETE ALL BOOKS")
        choice = input("Are you sure that you want to delete all books?"
                       " Enter 'Y' to confirm, any other character to"
                       " go back to the menu: ").upper()
        if choice == "Y" or choice == "'Y'":
            cursor.execute("""DELETE FROM books""")
            db.commit()
            print("\nAll books have been deleted.")
    else:
        print("\nWe are sorry, there are not books at the moment, you can "
              "add them selecting the option 2 from the menu.")


# Create a "while True" loop that stores the variable "menu_choice"; this
# variable will allow the user to select and operate the requested actions
# through the apposite functions recalled based on the selected option.
# In this loop I stored also the command to open/create the database called
# "ebookstore_db" and I incorporated all the codes into a try-except-finally
# block. In this way if something goes wrong the system will catch and raise
# the error but before that it will roll back any changes and in any case the
# database will be closed after each operation.
while True:
    db = sqlite3.connect("ebookstore_db")
    try:
        cursor = db.cursor()
        # Check if the table "books" exists.
        cursor.execute("""SELECT name FROM sqlite_master WHERE type = ?
            AND name = ?""", ("table", "books"))
        # If the table "books" doesn't exist, create and populate it.
        if cursor.fetchone() is None:
            create_table()
            populate_table()

        menu_choice = input("""\nBOOKSTORE MENU
1 - Display all books
2 - Enter book
3 - Update book
4 - Delete book
5 - Search books
6 - Delete all books
0 - Exit
Enter the number of your choice: """).strip()

        if menu_choice == "1":
            display_books()
        elif menu_choice == "2":
            insert_book()
        elif menu_choice == "3":
            update_book()
        elif menu_choice == "4":
            delete_book()
        elif menu_choice == "5":
            search_books()
        elif menu_choice == "6":
            delete_all()
        elif menu_choice == "0":
            print("\nThank you, goodbye!")
            quit()
        else:
            print("\nWe are sorry, you entered a wrong "
                  "choice, please try again.")

    except Exception as e:
        db.rollback()
        raise e

    finally:
        db.close()

from models import Book, DVD, LibraryItem, Magazine, Member


def main():
    print("=" * 65)
    print("       CAMPUS LIBRARY MANAGEMENT SYSTEM - DEMO RUN")
    print("=" * 65)
    print("\n--- 0. Abstract Class Instantiation Check ---")
    try:
        LibraryItem("Generic Item", 999)
    except TypeError as e:
        print(f"Verified: Cannot instantiate abstract LibraryItem directly.")
        print(f"Exception caught: {e}")

    # Create items (one of each concrete item type)
    book = Book("Python 101", 1, "A. Rao")
    magazine = Magazine("Tech Monthly", 2, 42)
    dvd = DVD("Inception", 3, 148)

    # Create two members (Bob has max_items=1 to easily test borrow limit)
    alice = Member("Alice", 101)
    bob = Member("Bob", 102, max_items=1)

    # -------------------------------------------------------------
    # 1. Borrowing with Error Handling (Already Borrowed)
    # -------------------------------------------------------------
    print("\n--- 1. Borrowing and 'Already Borrowed' Error Handling ---")
    try:
        alice.borrow(book)
        print("Success: Alice borrowed:", book.describe())
    except ValueError as e:
        print("Could not borrow:", e)

    # Bob attempts to borrow the same book
    try:
        bob.borrow(book)  # should fail: already borrowed
    except ValueError as e:
        print("Could not borrow (expected error):", e)

    # -------------------------------------------------------------
    # 2. Trigger Borrow-Limit and Not-Borrowed Errors
    # -------------------------------------------------------------
    print("\n--- 2. Borrow-Limit and Not-Borrowed Error Handling ---")

    # Bob borrows a magazine (reaches his limit of 1)
    try:
        bob.borrow(magazine)
        print("Success: Bob borrowed:", magazine.describe())
    except ValueError as e:
        print("Could not borrow:", e)

    # Bob attempts to borrow a DVD (exceeds limit of 1)
    try:
        bob.borrow(dvd)  # should fail: limit reached
    except ValueError as e:
        print("Could not borrow (expected error):", e)

    # Alice tries to return the DVD (which she never borrowed)
    try:
        alice.return_item(dvd)  # should fail: not in member's borrowed list
    except ValueError as e:
        print("Could not return (expected error):", e)

    # Return items with late fees
    print("\n--- Return Processing with Late Fees ---")
    fee_alice = alice.return_item(book, days_late=2)
    print(f"Alice returned '{book.title}' (2 days late) -> Late Fee: Rs {fee_alice}")

    fee_bob = bob.return_item(magazine, days_late=0)
    print(f"Bob returned '{magazine.title}' (on time) -> Late Fee: Rs {fee_bob}")

    # -------------------------------------------------------------
    # 3. Polymorphism: One Loop, No Type Checks
    # -------------------------------------------------------------
    print("\n--- 3. Polymorphism: Unified Interface for Different Item Types ---")
    items = [book, magazine, dvd]
    for item in items:
        # Polymorphic calls: late_fee() and describe() without any type inspect/if-checks
        print(f"{item.describe()} -> late fee for 3 days: Rs {item.late_fee(3)}")

    # -------------------------------------------------------------
    # 4. Class Attribute Shared by All Objects
    # -------------------------------------------------------------
    print("\n--- 4. Class vs Instance Attributes ---")
    print("Total items created (via LibraryItem.total_items):", LibraryItem.total_items)
    print("Total items created (via Book.total_items):", Book.total_items)

    # -------------------------------------------------------------
    # 5. Encapsulation Verification
    # -------------------------------------------------------------
    print("\n--- 5. Encapsulation Verification ---")
    try:
        # Direct access to private attribute will raise AttributeError
        _ = book.__available
    except AttributeError as e:
        print("Verified: Cannot access private '__available' directly from outside.")
        print(f"AttributeError caught: {e}")

    print("Proper access via public method is_available():", book.is_available())

    try:
        # Direct access to private borrowed list will raise AttributeError
        _ = alice.__borrowed
    except AttributeError as e:
        print("Verified: Cannot access private '__borrowed' directly from outside.")
        print(f"AttributeError caught: {e}")

    print("Proper access via public method borrowed_titles():", alice.borrowed_titles())

    print("\n" + "=" * 65)
    print("                     DEMO RUN COMPLETED")
    print("=" * 65)


if __name__ == "__main__":
    main()


from abc import ABC, abstractmethod


class LibraryItem(ABC):
    
    total_items = 0  # Class attribute, shared across all items

    def __init__(self, title: str, item_id: int):
        self.title = title
        self.item_id = item_id
        self.__available = True  # Private attribute: tracks availability
        LibraryItem.total_items += 1  # Increment global item counter

    def is_available(self) -> bool:
        return self.__available

    def mark_borrowed(self) -> None:
        self.__available = False

    def mark_returned(self) -> None:
        self.__available = True

    @abstractmethod
    def late_fee(self, days_late: int) -> int:
        pass

    def describe(self) -> str:
        return f"LibraryItem: {self.title} (ID {self.item_id})"


class Book(LibraryItem):

    DAILY_RATE = 2

    def __init__(self, title: str, item_id: int, author: str):
        super().__init__(title, item_id)
        self.author = author

    def late_fee(self, days_late: int) -> int:
        return max(0, days_late) * self.DAILY_RATE

    def describe(self) -> str:
        return f"Book: {self.title} by {self.author} (ID {self.item_id})"


class Magazine(LibraryItem):
    DAILY_RATE = 1

    def __init__(self, title: str, item_id: int, issue_number: int):
        super().__init__(title, item_id)
        self.issue_number = issue_number

    def late_fee(self, days_late: int) -> int:
        return max(0, days_late) * self.DAILY_RATE

    def describe(self) -> str:
        return f"Magazine: {self.title} Issue #{self.issue_number} (ID {self.item_id})"


class DVD(LibraryItem):
    DAILY_RATE = 5

    def __init__(self, title: str, item_id: int, duration_minutes: int):
        super().__init__(title, item_id)
        self.duration_minutes = duration_minutes

    def late_fee(self, days_late: int) -> int:
        return max(0, days_late) * self.DAILY_RATE

    def describe(self) -> str:
        return f"DVD: {self.title} ({self.duration_minutes} mins) (ID {self.item_id})"


class Member:

    def __init__(self, name: str, member_id: int, max_items: int = 3):
        self.name = name
        self.member_id = member_id
        self.max_items = max_items
        self.__borrowed = []  # Private list of currently borrowed items

    def borrow(self, item: LibraryItem) -> None:
        if not item.is_available():
            raise ValueError(f"Cannot borrow '{item.title}': Item is already borrowed.")
        if len(self.__borrowed) >= self.max_items:
            raise ValueError(
                f"Cannot borrow '{item.title}': {self.name} has reached the borrowing limit of {self.max_items} item(s)."
            )
        item.mark_borrowed()
        self.__borrowed.append(item)

    def return_item(self, item: LibraryItem, days_late: int = 0) -> int:
        if item not in self.__borrowed:
            raise ValueError(
                f"Cannot return '{item.title}': Item was not borrowed by {self.name}."
            )
        item.mark_returned()
        self.__borrowed.remove(item)
        return item.late_fee(days_late)

    def borrowed_titles(self) -> list[str]:
        return [item.title for item in self.__borrowed]


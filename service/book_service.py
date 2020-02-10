from exception.bookstore_exception import BookNotFoundException, SaleOperationException, BadRequestException


class BookService(object):
    def __init__(self, repository):
        self.repository = repository

    def get_book(self, book_id):
        book = self.repository.get_book(book_id)
        if book is None:
            raise BookNotFoundException("book not found")
        return self.repository.get_book(book_id)

    def query_book(self, query):
        return self.repository.query_book(query)

    def get_total_sold_by_category(self):
        return self.repository.get_total_sold_by_category()

    def count_book(self, query):
        return self.repository.count_book(query)

    def create_book(self, book):
        return self.repository.create_book(book)

    def update_book(self, book):
        book_from_db = self.repository.get_book(book.id)
        if book_from_db is None:
            raise BookNotFoundException("book not found")
        return self.repository.update_book(book)

    def delete_book(self, book_id):
        book = self.repository.get_book(book_id)
        if book is None:
            raise BookNotFoundException("book not found")
        self.repository.delete_book(book_id)

    def sale_book(self, book_id, amount):
        if amount <= 0:
            raise BadRequestException("amount must be positive integer")
        book = self.get_book(book_id)
        if book.current_amount < amount:
            raise SaleOperationException("Insufficient amount")
        book.current_amount = book.current_amount - amount
        book.sold_amount = book.sold_amount + amount
        self.repository.update_book(book)

    def fulfill_book(self, book_id, amount):
        if amount <= 0:
            raise BadRequestException("amount must be positive integer")
        book = self.get_book(book_id)
        book.current_amount = book.current_amount + amount
        self.repository.update_book(book)

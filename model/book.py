class Book(object):
    def __init__(self, book_id=None, title=None, synopsis=None, isbn10=None, isbn13=None,
                 language=None, publisher=None, edition=None, paperback_price=None, ebook_price=None,
                 created_time=None, modified_time=None, sold_amount=0, current_amount=0, category=None):
        self.id = book_id
        self.title = title
        self.synopsis = synopsis
        self.isbn10 = isbn10
        self.isbn13 = isbn13
        self.language = language
        self.publisher = publisher
        self.edition = edition
        self.paperback_price = paperback_price
        self.ebook_price = ebook_price
        self.created_time = created_time
        self.modified_time = modified_time
        self.sold_amount = sold_amount
        self.current_amount = current_amount
        self.category = category

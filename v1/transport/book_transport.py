from pydantic import BaseModel
from datetime import datetime


class BookTransport(BaseModel):
    id: str = None
    title: str
    synopsis: str
    isbn10: str = None
    isbn13: str = None
    language: str
    publisher: str
    edition: str = None
    paperback_price: float = None
    ebook_price: float = None
    created_time: datetime = None
    modified_time: datetime = None
    sold_amount: int = 0
    current_amount: int = 0
    category: str


class BestSellerTransport(object):
    def __init__(self, book_id, title, category, sold_amount):
        self.id = book_id
        self.title = title
        self.category = category
        self.sold_amount = sold_amount


class TotalSoldByCategoryTransport(object):
    def __init__(self, category, total_sold_amount):
        self.category = category
        self.total_sold_amount = total_sold_amount


class SaleBookTransport(BaseModel):
    amount: int


class FulfillBookTransport(BaseModel):
    amount: int

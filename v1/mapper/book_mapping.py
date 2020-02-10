from model.book import Book
from v1.transport.book_transport import BookTransport, BestSellerTransport, TotalSoldByCategoryTransport


def to_model(transport):
    return Book(book_id=transport.id,
                title=transport.title,
                synopsis=transport.synopsis,
                isbn10=transport.isbn10,
                isbn13=transport.isbn13,
                language=transport.language,
                publisher=transport.publisher,
                edition=transport.edition,
                paperback_price=transport.paperback_price,
                ebook_price=transport.ebook_price,
                sold_amount=transport.sold_amount,
                current_amount=transport.current_amount,
                category=transport.category,
                created_time=transport.created_time,
                modified_time=transport.modified_time)


def to_transport(model):
    transport = BookTransport(**model.__dict__)
    return transport


def report_to_transport(report):
    return TotalSoldByCategoryTransport(report.category, report.total_sold_amount)


def to_bast_seller_transport(model):
    return BestSellerTransport(model.id, model.title, model.category, model.sold_amount)

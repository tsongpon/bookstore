import os
from fastapi import FastAPI, Header
from v1.transport.book_transport import BookTransport as BookTransportV1
from v1.transport.book_transport import SaleBookTransport as SaleBookTransportV1
from v1.transport.book_transport import FulfillBookTransport as FulfillBookTransportV1
from service.book_service import BookService
from repository.book_repository import BookRepository
from v1.mapper import book_mapping
from starlette.status import *
from yoyo import read_migrations
from yoyo import get_backend
from exception.bookstore_exception import *
import psycopg2
from psycopg2 import pool
from starlette.responses import JSONResponse
from starlette.responses import Response
import hashlib

db_host = os.getenv('DB_HOST', 'localhost')
db_user = os.getenv('DB_USER', 'postgres')
db_port = os.getenv('DB_PORT', 5432)
db_pass = os.getenv('DB_PASSWORD', 'pingu123')

backend_url = 'postgresql://{user}:{password}@{host}:{port}/bookstore'.format(user=db_user,
                                                                              password=db_pass,
                                                                              host=db_host,
                                                                              port=db_port)
backend = get_backend(backend_url)
migrations = read_migrations('./migrations')

with backend.lock():
    backend.apply_migrations(backend.to_apply(migrations))

api = FastAPI()
api.title = "Book Store API"

connection_pool = psycopg2.pool.SimpleConnectionPool(2, 20,
                                                     user=db_user, password=db_pass,
                                                     host=db_host, port=int(db_port),
                                                     database="bookstore")

bookRepository = BookRepository(connection_pool)
bookService = BookService(bookRepository)


def generate_etag(book_model):
    return hashlib.md5(str(book_model.modified_time).encode('utf-8')).hexdigest()


@api.get("/ping")
def ping():
    return {"ping": "ok"}


@api.post("/v1/books", status_code=HTTP_201_CREATED)
def create_book(book_transport: BookTransportV1):
    book_model = book_mapping.to_model(book_transport)
    created = bookService.create_book(book_model)
    return book_mapping.to_transport(created)


@api.get("/v1/books")
def query_book(limit: int = 5, offset: int = 0, title: str = None, order_field: str = None):
    query = {'limit': limit, 'offset': offset, 'title': title, 'order_by': order_field}
    books = bookService.query_book(query)
    book_transports = [book_mapping.to_transport(each) for each in books]
    total_count = bookService.count_book(query)
    response_body = {'total': total_count, 'size': len(book_transports), 'data': book_transports}
    return response_body


@api.get("/v1/books/reports/bestseller")
def get_best_seller(limit: int = 5, offset: int = 0, title: str = None):
    query = {'limit': limit, 'offset': offset, 'title': title, 'order_by': 'soldamount'}
    books = bookService.query_book(query)
    report = [book_mapping.to_bast_seller_transport(each) for each in books]
    total_count = bookService.count_book(query)
    response = {'total': total_count, 'size': len(report), 'data': report}
    return response


@api.get("/v1/books/reports/totalsoldbycategory")
def get_total_sold_by_category():
    report = bookService.get_total_sold_by_category()
    report_transports = [book_mapping.report_to_transport(each) for each in report]
    return report_transports


@api.get("/v1/books/{book_id}")
def get_book(book_id: str, response: Response):
    book_model = bookService.get_book(book_id)
    response.headers["etag"] = generate_etag(book_model)
    return book_mapping.to_transport(book_model)


@api.put("/v1/books/{book_id}")
def update_book(book_transport: BookTransportV1, book_id: str, if_match: str = Header(None)):
    book_from_db = bookService.get_book(book_id)
    etag_from_book_from_db = generate_etag(book_from_db)
    if if_match != etag_from_book_from_db:
        raise PreconditionFailException("Conflict")
    book_model = book_mapping.to_model(book_transport)
    updated = bookService.update_book(book_model)
    return book_mapping.to_transport(updated)


@api.post("/v1/books/{book_id}/sale")
def sale_book(sale_transport: SaleBookTransportV1, book_id: str):
    bookService.sale_book(book_id, sale_transport.amount)
    return {"status": "OK"}


@api.post("/v1/books/{book_id}/fulfill")
def fulfill_book(fulfill_transport: FulfillBookTransportV1, book_id: str):
    bookService.fulfill_book(book_id, fulfill_transport.amount)
    return {"status": "OK"}


@api.delete("/v1/books/{book_id}")
def delete_book(book_id: str):
    bookService.delete_book(book_id)
    return {"status": "OK"}


@api.exception_handler(BookNotFoundException)
def not_found_exception_handler(request, exc):
    return JSONResponse(status_code=HTTP_404_NOT_FOUND, content={"message": str(exc)})


@api.exception_handler(PreconditionFailException)
def conflict_exception_handler(request, exc):
    return JSONResponse(status_code=HTTP_412_PRECONDITION_FAILED, content={"message": str(exc)})


@api.exception_handler(SaleOperationException)
def sale_exception_handler(request, exc):
    return JSONResponse(status_code=HTTP_400_BAD_REQUEST, content={"message": str(exc)})


@api.exception_handler(BadRequestException)
def bad_request_exception_handler(request, exc):
    return JSONResponse(status_code=HTTP_400_BAD_REQUEST, content={"message": str(exc)})

import uuid
from model.book import Book
from model.report import TotalSoldByCategory
from datetime import datetime


class BookRepository(object):
    columns = """id, title, synopsis, isbn10, isbn13, language, publisher, edition,
                    paperbackprice, ebookprice, createdtime, modifiedtime, soldamount, currentamount, category"""

    def __init__(self, db_connection_pool):
        self.db_connection_pool = db_connection_pool
        self.storage = {}

    def get_book(self, book_id):
        book_from_db = None
        conn = self.db_connection_pool.getconn()
        try:
            with conn.cursor() as cursor:
                sql = """
                        SELECT {columns}
                        FROM book WHERE id=%s
                    """.format(columns=BookRepository.columns)
                cursor.execute(sql, (book_id,))
                result = cursor.fetchone()
                if result is not None:
                    book_from_db = Book(result[0], result[1], result[2], result[3],
                                        result[4], result[5], result[6],
                                        result[7], result[8], result[9],
                                        result[10], result[11], result[12], result[13], result[14])
        finally:
            self.db_connection_pool.putconn(conn)
        return book_from_db

    def count_book(self, query):
        count = None
        conn = self.db_connection_pool.getconn()
        try:
            with conn.cursor() as cursor:
                filter_sql = ""
                if query['title'] is not None:
                    filter_sql = " WHERE title like '%{}%' ".format(query['title'])
                sql = "SELECT COUNT(id) as count FROM book {filter}".format(filter=filter_sql)
                cursor.execute(sql)
                result = cursor.fetchone()
                if result is not None:
                    count = result[0]
        finally:
            self.db_connection_pool.putconn(conn)
        return count

    def query_book(self, query):
        books = []
        conn = self.db_connection_pool.getconn()
        try:
            with conn.cursor() as cursor:
                filter_sql = ""
                if query['title'] is not None:
                    filter_sql = " WHERE title like '%{}%' ".format(query['title'])
                if query['order_by'] is None:
                    query['order_by'] = 'createdtime'
                sql = "SELECT {columns} FROM book {filter} ORDER BY {order_field} DESC LIMIT {limit} OFFSET {offset} "\
                    .format(columns=BookRepository.columns, limit=query['limit'],
                            offset=query['offset'], filter=filter_sql, order_field=query['order_by'])
                cursor.execute(sql)
                result = cursor.fetchall()
                for each in result:
                    books.append(Book(each[0], each[1], each[2], each[3], each[4],
                                      each[5], each[6], each[7], each[8],
                                      each[9], each[10], each[11], each[12],
                                      each[13], each[14]))
        finally:
            self.db_connection_pool.putconn(conn)
        return books

    def create_book(self, book):
        new_id = str(uuid.uuid4())
        book.id = new_id
        now = datetime.now()
        book.created_time = now
        book.modified_time = now
        conn = self.db_connection_pool.getconn()
        try:
            with conn.cursor() as cursor:
                sql = """INSERT INTO book ({column})
                             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""".format(column=BookRepository.columns)
                cursor.execute(sql, (book.id, book.title, book.synopsis, book.isbn10, book.isbn13,
                                     book.language, book.publisher, book.edition, book.paperback_price, book.ebook_price,
                                     book.created_time, book.modified_time, book.sold_amount, book.current_amount, book.category))
            conn.commit()
        finally:
            self.db_connection_pool.putconn(conn)
        return book

    def update_book(self, book):
        conn = self.db_connection_pool.getconn()
        try:
            with conn.cursor() as cursor:
                sql = """UPDATE book
                            SET title=%s, 
                                synopsis=%s ,
                                isbn10=%s,
                                isbn13=%s,
                                language=%s,
                                publisher=%s,
                                edition=%s,
                                paperbackprice=%s,
                                ebookprice=%s,
                                modifiedtime=%s,
                                soldamount=%s,
                                currentamount=%s,
                                category=%s
                            WHERE id=%s"""
                cursor.execute(sql, (book.title, book.synopsis, book.isbn10, book.isbn13, book.language,
                                     book.publisher, book.edition, book.paperback_price, book.paperback_price,
                                     datetime.now(), book.sold_amount, book.current_amount, book.category, book.id))
            conn.commit()
        finally:
            self.db_connection_pool.putconn(conn)
        return self.get_book(book.id)

    def delete_book(self, book_id):
        conn = self.db_connection_pool.getconn()
        try:
            with conn.cursor() as cursor:
                sql = "DELETE FROM book WHERE id=%s"
                cursor.execute(sql, (book_id,))
            conn.commit()
        finally:
            self.db_connection_pool.putconn(conn)

    def get_total_sold_by_category(self):
        report = []
        conn = self.db_connection_pool.getconn()
        try:
            with conn.cursor() as cursor:
                sql = "SELECT category, SUM (soldamount) as total FROM book GROUP BY category ORDER BY total DESC"
                cursor.execute(sql)
                result = cursor.fetchall()
                for each in result:
                    report.append(TotalSoldByCategory(each[0], each[1]))
        finally:
            self.db_connection_pool.putconn(conn)
        return report

    def delete_all_book(self):
        conn = self.db_connection_pool.getconn()
        try:
            with conn.cursor() as cursor:
                sql = "DELETE FROM book"
                cursor.execute(sql)
            conn.commit()
        finally:
            self.db_connection_pool.putconn(conn)

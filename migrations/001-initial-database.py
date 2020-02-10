from yoyo import step

create_table = """create table book
(
    id varchar(36) not null
    primary key,
    title varchar(255) not null,
    synopsis text null,
    isbn10 varchar(15) null,
    isbn13 varchar(15) null,
    language varchar(30) not null,
    publisher varchar(255) not null,
    edition varchar(50) null,
    soldamount int not null default 0,
    currentamount int not null default 0,
    paperbackprice float null,
    ebookprice float null,
    createdtime timestamp not null,
    modifiedtime timestamp not null,
    category varchar(255) not null,
    constraint book_isbn10_uindex unique (isbn10),
    constraint book_isbn13_uindex unique (isbn13)
)
"""

rollback = "drop table book"

create_index_title = "create index book_title_index on book (title)"

step(create_table, rollback)

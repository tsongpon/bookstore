from yoyo import step

__depends__ = {'001-initial-database'}

create_index_title = "create index book_title_index on book (title)"
rollback = "drop index book_title_index "

step(create_index_title, rollback)

from TelegramTextApp.utils.database import SQL_request as SQL  # type: ignore

SQL("""
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    author TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT NOT NULL DEFAULT 'active'
);
    """)


def add_book(name: str, author: str | None = None) -> None:
    SQL(f"""
        INSERT INTO books (name, author, status)
        VALUES ('{name}', '{author}', 'active');
        """)


def list_books() -> list:
    books = SQL("SELECT * FROM books WHERE status = 'active';", fetch="all")
    return books


try:
    SQL("""
    ALTER TABLE TTA 
    ADD COLUMN pages JSON;
    """)
except Exception as e:
    pass

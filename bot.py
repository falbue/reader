import TelegramTextApp
from TelegramTextApp import config  # type: ignore
import os
import re
import database as db

book_path = config.BOOKS_PATH
os.makedirs(book_path, exist_ok=True)


def list_books(tta):
    books = db.list_books()
    keyboard = {}
    for book in books:
        keyboard[f"read_book|{book['id']}"] = book["name"]
    return keyboard


def read_book(tta):
    page = tta["book_page"]
    if page is None:
        page = 0
    else:
        page = int(page)

    if tta.get("select_page"):
        try:
            page = int(tta["select_page"])
        except Exception as e:
            print("Не удалось обработать номер страницы:", e)
            return {"error": "⛔ Некорректный номер страницы"}

    book_id = tta["book_id"]
    book = db.SQL("SELECT * FROM books WHERE id = ?", (book_id,), fetch="one")
    book_file = os.path.join(book_path, f"{book['id']}.txt")
    if not os.path.exists(book_file):
        return {"book_text": "Книга не найдена"}
    with open(book_file, "r", encoding="utf-8") as f:
        full_text = f.read()

    def paginate(text: str, limit: int = 500):
        # Build chunks up to limit without splitting words; tokens keep trailing spaces to preserve spacing.
        tokens = re.findall(r"\S+\s*", text)
        if not tokens:
            return [""]

        pages = []
        current = ""
        for token in tokens:
            if not current:
                current = token
                continue
            if len(current) + len(token) <= limit:
                current += token
            else:
                pages.append(current.rstrip())
                current = token
        if current:
            pages.append(current.rstrip())
        return pages

    pages = paginate(full_text)
    if page < 0 or page >= len(pages):
        page = 0
    return {
        "book_text": pages[page],
        "prev_page": max(0, page - 1),
        "next_page": min(len(pages) - 1, page + 1),
        "book_page": page,
        "total_pages": len(pages),
    }


if __name__ == "__main__":
    TelegramTextApp.start()  # type: ignore

import sqlite3

def show(title, rows):
    print(f"\n{title}")
    for r in rows:
        print("  ", r)

conn = None
try:
    # 1-2. Створення БД «Туристичне агентство» та підключення
    conn = sqlite3.connect("travel_agency.db")
    cur = conn.cursor()
    print("Підключення до бази даних успішне")

    # 3. Створення таблиці «Тури» (DROP — щоб скрипт можна було запускати повторно)
    cur.execute("DROP TABLE IF EXISTS tours")
    cur.execute("""
    CREATE TABLE tours (
        id         INTEGER PRIMARY KEY,
        name       VARCHAR(255) NOT NULL,
        country    VARCHAR(100) NOT NULL,
        duration   INTEGER      NOT NULL,   -- тривалість, днів
        price      REAL         NOT NULL,   -- ціна, грн
        start_date DATE                     -- дата початку (РРРР-ММ-ДД)
    )
    """)
    conn.commit()
    print("Таблицю 'tours' створено")

    # 4. Вставка даних
    tours = [
        (1, "Відпочинок на Егейському морі", "Греція",     7, 28500.00, "2026-06-10"),
        (2, "Альпійські вершини",            "Австрія",   10, 45200.00, "2026-01-15"),
        (3, "Античний Рим",                  "Італія",     5, 32000.00, "2026-04-20"),
        (4, "Анталія All Inclusive",         "Туреччина",  8, 24900.00, "2026-07-01"),
        (5, "Карпатські стежки",             "Україна",    4,  9800.00, "2026-08-05"),
        (6, "Казки Праги",                   "Чехія",      6, 21000.00, "2026-05-12"),
    ]
    cur.executemany("INSERT INTO tours VALUES (?, ?, ?, ?, ?, ?)", tours)
    conn.commit()
    print(f"Вставлено рядків: {cur.rowcount}")
    show("Усі тури після вставки:", cur.execute("SELECT * FROM tours").fetchall())
    # 5.Оновлення
    cur.execute("UPDATE tours SET price = ROUND(price * 0.9, 2) WHERE duration > 7")
    print(f"\nЗнижку 10% застосовано до {cur.rowcount} турів")
    cur.execute("UPDATE tours SET duration = 6 WHERE name = ?", ("Античний Рим",))
    conn.commit()
    show("Після оновлення:", cur.execute("SELECT * FROM tours").fetchall())
    # 6.Видалення
    cur.execute("DELETE FROM tours WHERE price < ?", (10000,))
    conn.commit()
    print(f"\nВидалено рядків: {cur.rowcount}")
    show("Після видалення:", cur.execute("SELECT * FROM tours").fetchall())

    # 7.Вибірки з умовами та сортуванням
    show("Усі тури за ціною (зростання):",
         cur.execute("SELECT name, country, price FROM tours ORDER BY price ASC").fetchall())
    show("Тури від 6 днів, за тривалістю (спадання):",
         cur.execute("SELECT name, duration FROM tours WHERE duration >= 6 "
                     "ORDER BY duration DESC").fetchall())
    show("Тури, назва яких починається на «А», за ціною:",
         cur.execute("SELECT name, country, price FROM tours WHERE name LIKE 'А%' "
                     "ORDER BY price").fetchall())
    show("Тури до Італії або Греції:",
         cur.execute("SELECT name, country FROM tours "
                     "WHERE country IN ('Італія', 'Греція')").fetchall())
    show("Тури з ціною 20000–30000 грн, за датою початку:",
         cur.execute("SELECT name, price, start_date FROM tours "
                     "WHERE price BETWEEN 20000 AND 30000 ORDER BY start_date").fetchall())

except sqlite3.Error as error:
    print("Помилка роботи з SQLite:", error)
finally:
    if conn:
        conn.close()
        print("\nЗ'єднання з базою даних закрито")

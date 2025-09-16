import sqlite3
import os


def create_database():
    if os.path.exists('my_database.db'):
        os.remove('my_database.db')
    
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute("""CREATE TABLE products (
            product_id INTEGER PRIMARY KEY,
            name VARCHAR(100),
            price DECIMAL(10, 2)
        );""")

        cursor.execute("""CREATE TABLE customers (
            customer_id INTEGER PRIMARY KEY,
            city VARCHAR(100)
        );""")

        cursor.execute("""CREATE TABLE orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            product_id INTEGER,
            quantity INTEGER,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        );""")

        cursor.execute("""INSERT INTO products VALUES 
            (1, 'Флешка', 1000), 
            (2, 'Мышь', 2500), 
            (3, 'Клавиатура', 5000);""")
        
        cursor.execute("""INSERT INTO customers VALUES 
            (101, 'Москва'), 
            (102, 'Самара'), 
            (103, 'Москва');""")
        
        cursor.execute("""INSERT INTO orders VALUES 
            (1, 101, 1, 2), 
            (2, 103, 3, 1), 
            (3, 101, 2, 1), 
            (4, 103, 1, 3);""")
        
        conn.commit()
        print("База данных успешно создана и заполнена данными!")
        
        print("\nСодержимое таблицы products:")
        cursor.execute("SELECT * FROM products")
        for row in cursor.fetchall():
            print(row)
        
        print("\nСодержимое таблицы customers:")
        cursor.execute("SELECT * FROM customers")
        for row in cursor.fetchall():
            print(row)
        
        print("\nСодержимое таблицы orders:")
        cursor.execute("SELECT * FROM orders")
        for row in cursor.fetchall():
            print(row)
            
    except sqlite3.Error as e:
        conn.rollback()
        print(f"Ошибка при создании БД: {e}")
    finally:
        conn.close()


def query_database():
    """Функция для выполнения запросов к базе данных"""
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    
    try:
        print("\n" + "="*50)
        print("Общая стоимость заказов:")
        cursor.execute("""
            SELECT o.order_id, p.name, o.quantity, p.price, 
                   (o.quantity * p.price) as total_price
            FROM orders o
            JOIN products p ON o.product_id = p.product_id
            ORDER BY o.order_id
        """)
        
        for row in cursor.fetchall():
            print(f"Заказ {row[0]}: {row[1]} x{row[2]} = {row[4]} руб.")
            
    except sqlite3.Error as e:
        print(f"Ошибка при выполнении запроса: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    create_database()
    query_database()

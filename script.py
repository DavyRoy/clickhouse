from clickhouse_driver import Client
from datetime import datetime

# Подключение к ClickHouse
client = Client('localhost', user='sergey', password='290315')

# Генерация тестовых данных с преобразованием строк в datetime
users_data = [
    (1, 'Иван', 'ivan@example.com', datetime(2024, 1, 1, 10, 0, 0)),
    (2, 'Мария', 'maria@example.com', datetime(2024, 2, 1, 12, 0, 0))
]

products_data = [
    (1, 'Ноутбук', 'Электроника', 75000, datetime(2024, 1, 5, 15, 30, 0)),
    (2, 'Клавиатура', 'Компьютерные аксессуары', 3000, datetime(2024, 2, 10, 10, 15, 0))
]

orders_data = [
    (1, 1, 1, 1, 75000, datetime(2024, 3, 1, 14, 0, 0)),
    (2, 2, 2, 2, 6000, datetime(2024, 3, 2, 16, 30, 0))
]

# Функция загрузки данных в ClickHouse
def insert_data(table, data):
    query = f"INSERT INTO {table} VALUES"
    client.execute(query, data)

# Загрузка данных
insert_data('users', users_data)
insert_data('products', products_data)
insert_data('orders', orders_data)

print("✅ Данные успешно загружены!")

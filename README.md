# Clickhouse
---

### Задание 1 - Введение в ClickHouse

1. `Установить ClickHouse в Docker: Запустить ClickHouse через docker-compose, Проверить, что контейнер работает.`
2. `Создать свою первую базу данных: Подключиться к ClickHouse, Проверить, что база создана.`
3. `Дополнительно: Подключиться к ClickHouse через DBeaver, Добавить скриншот успешного подключения`

``` ~Решение~
1.
nano docker-compose.yml
....
version: '3.8'

services:
  clickhouse:
    image: clickhouse/clickhouse-server:latest
    container_name: clickhouse
    restart: always
    ports:
      - "8123:8123"
      - "9000:9000"
    volumes:
      - clickhouse_data:/var/lib/clickhouse
    environment:
      CLICKHOUSE_USER: name
      CLICKHOUSE_PASSWORD: password
      CLICKHOUSE_DB: test_db

volumes:
  clickhouse_data:
....
docker compose up -d
docker ps 
....
9c03c1169a7c   clickhouse/clickhouse-server:latest   "/entrypoint.sh"         49 minutes ago   Up 49 minutes   0.0.0.0:8123->8123/tcp, :::8123->8123/tcp, 0.0.0.0:9000->9000/tcp, :::9000->9000/tcp, 9009/tcp   clickhouse
....
2.
docker exec -it clickhouse clickhouse-client -u admin --password admin123
SHOW DATABASES;
```

`Cкриншоты
![DBeaver](https://github.com/DavyRoy/clickhouse/blob/main/images/DBeaver.png)

---

### Задание 2 - Основы работы с ClickHouse

1. `Создать таблицы users, orders, products с разными типами данных: Используй типы данных UInt32, String, Float64, DateTime, Nullable.`
2. `Написать SQL-запросы для вставки и удаления данных: Добавь даннык в таблицы users, orders, products.`

``` ~Решение~
1.
CREATE TABLE users (
    id UInt32,
    name String,
    email String,
    created_at DateTime,
    balance Float64
) ENGINE = MergeTree()
ORDER BY id;
....
CREATE TABLE orders (
    order_id UInt32,
    user_id UInt32,
    total_amount Float64,
    order_date DateTime
) ENGINE = MergeTree()
ORDER BY order_id;
....
CREATE TABLE products (
    product_id UInt32,
    name String,
    price Float64,
    launch_date DateTime,
    discontinued Nullable(DateTime)
) ENGINE = MergeTree()
ORDER BY product_id;
2.
INSERT INTO users (id, name, email, created_at, balance) VALUES
(1, 'Alice', 'alice@example.com', '2025-02-17 10:00:00', 100.5),
(2, 'Bob', 'bob@example.com', '2025-02-17 11:00:00', 200.0);
....
INSERT INTO orders (order_id, user_id, total_amount, order_date) VALUES
(1, 1, 50.0, '2025-02-17 10:30:00'),
(2, 2, 75.0, '2025-02-17 11:45:00');
....
INSERT INTO products (product_id, name, price, launch_date, discontinued) VALUES
(1, 'Laptop', 1200.5, '2025-01-01 10:00:00', NULL),
(2, 'Smartphone', 799.99, '2025-02-01 12:00:00', NULL);
....
SHOW TABLES;

SHOW TABLES

Query id: 2c567405-ff36-4958-813e-b92c074aca80

   ┌─name─────┐
1. │ orders   │
2. │ products │
3. │ users    │
   └──────────┘

3 rows in set. Elapsed: 0.006 sec. 
```

`Cкриншоты
![DB tables](https://github.com/DavyRoy/clickhouse/blob/main/images/DB%20tables.png)

---

### Задание 3 - Оптимизация хранения данных в ClickHouse

1. `Создай таблицу с несколькими индексами .`
2. `Напиши запрос для анализа.`


``` ~Решение~
1.
CREATE TABLE products (
    product_id UInt32,
    name String,
    price Float64,
    category String
) ENGINE = MergeTree()
PRIMARY KEY (product_id)
PARTITION BY category
ORDER BY (price, product_id);
2.
EXPLAIN SELECT * FROM products WHERE category = 'Electronics' AND price > 500;
....
```

`Cкриншоты
![Скриншот](ссылка на скриншот)`

---

### Задание 4 - Запросы и аналитика в ClickHouse

1. ` Написать запрос, который покажет топ-10 продуктов по продажам
Твой запрос должен: соединить sales и products, посчитать сумму продаж (SUM(amount)) по каждому товару, отсортировать по убыванию (ORDER BY total_revenue DESC), вывести ТОП-10 товаров (LIMIT 10).`

``` ~Решение~
1.
SELECT 
    p.product_id,
    p.product_name,
    SUM(s.amount) AS total_revenue
FROM sales AS s
JOIN products AS p ON s.product_id = p.product_id
GROUP BY p.product_id, p.product_name
ORDER BY total_revenue DESC
LIMIT 10;
....
```

`Скриншоты
![Скриншот ](ссылка на скриншот)`

---

### Задание 5 - Администрирование

1. `Сделать бэкап`
2. `Создать бэкап через SQL`
3. `Восстановить данные`
4. `Репликация`

``` ~Решение~
1.
docker stop clickhouse
tar -cvzf clickhouse_backup.tar.gz /var/lib/clickhouse/
docker start clickhouse
docker stop clickhouse
tar -xvzf clickhouse_backup.tar.gz -C /
docker start clickhouse
2.
BACKUP DATABASE my_db TO Disk('backup_disk', 'my_db_backup');
3.
RESTORE DATABASE my_db FROM Disk('backup_disk', 'my_db_backup');
4.
docker network create clickhouse_net
....
docker run -d --name clickhouse1 --network clickhouse_net \
  -e CLICKHOUSE_USER=default -e CLICKHOUSE_PASSWORD=password \
  -e CLICKHOUSE_REPLICA=replica1 -e CLICKHOUSE_SHARD=shard1 \
  -p 8123:8123 -p 9000:9000 clickhouse/clickhouse-server
....
docker run -d --name clickhouse2 --network clickhouse_net \
  -e CLICKHOUSE_USER=default -e CLICKHOUSE_PASSWORD=password \
  -e CLICKHOUSE_REPLICA=replica2 -e CLICKHOUSE_SHARD=shard1 \
  clickhouse/clickhouse-server
....
CREATE TABLE sales (
    sale_id UInt32,
    product_id UInt32,
    amount Float32,
    sale_date Date
) ENGINE = ReplicatedMergeTree('/clickhouse/tables/sales', 'replica1')
ORDER BY sale_date;
....
```

`Скриншоты
![Скриншот ](ссылка на скриншот)`

---

### Задание 6 - Мини-проект

1. `Сделать базы данных для аналитики`
2. `Python-скрипт для загрузки данных`
3. `Визуализация данных в Grafana`

``` ~Решение~
1.
CREATE TABLE users (
    user_id UInt32,
    name String,
    email String,
    created_at DateTime
) ENGINE = MergeTree()
ORDER BY user_id;

CREATE TABLE products (
    product_id UInt32,
    name String,
    category String,
    price Float64,
    created_at DateTime
) ENGINE = MergeTree()
ORDER BY product_id;

CREATE TABLE orders (
    order_id UInt32,
    user_id UInt32,
    product_id UInt32,
    quantity UInt8,
    total_price Float64,
    order_date DateTime
) ENGINE = MergeTree()
ORDER BY order_id;
2.
from clickhouse_driver import Client
from datetime import datetime

client = Client('localhost', user='sergey', password='290315')

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

def insert_data(table, data):
    query = f"INSERT INTO {table} VALUES"
    client.execute(query, data)

insert_data('users', users_data)
insert_data('products', products_data)
insert_data('orders', orders_data)

print("✅ Данные успешно загружены!")

3.
docker run -d --name=grafana -p 3000:3000 grafana/grafana
SELECT products.name, SUM(orders.quantity) as total_sales
FROM orders
JOIN products ON orders.product_id = products.product_id
GROUP BY products.name
ORDER BY total_sales DESC
LIMIT 5;

....
```

`Скриншоты
![grafana](https://github.com/DavyRoy/clickhouse/blob/main/images/grafana.png)

---

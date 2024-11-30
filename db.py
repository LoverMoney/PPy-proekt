import redis  
from faker import Faker  
import random
# Инициализация \ Redis клиента  
r = redis.Redis(host='localhost', port=6379, db=0)  

# Инициализация Faker  
fake = Faker()  

products=[]

# Функция для генерации данных для пользователей  
def create_users(num):  
    for _ in range(num):  
        user_id = fake.uuid4()  # Генерируем уникальный идентификатор  
        r.hset(f"user:{user_id}", mapping={  
            'name': fake.name(),  
            'email': fake.email(),  
            'address': fake.address(),  
            'created_at': fake.date_time_this_decade().isoformat()  
        })  

# Функция для генерации данных для продуктов  
def create_products(num):  
    for _ in range(num):  
        product_id = fake.uuid4()
        products.append(product_id)  
        r.hset(f"product:{product_id}", mapping={  
            'id': product_id,
            'name': fake.word(),  
            'description': fake.text(),  
            'price': fake.random_number(digits=2),  
            'created_at': fake.date_time_this_decade().isoformat()  
        })  

# Функция для генерации данных для заказов  
def create_orders(num):  
    for _ in range(num):  
        order_id = fake.uuid4()  
        # Случайный выбор пользователя и продукта (это предполагает, что они уже существуют)  
        user_id = fake.uuid4()  # Не забудьте заменить это на существующий user_id  
        product_id = products[random.randint(0,99)]  # Не забудьте заменить это на существующий product_id  
        r.hset(f"order:{order_id}", mapping={  
            'user_id': user_id,  
            'product_id': product_id,  
            'quantity': fake.random_int(min=1, max=5),  
            'created_at': fake.date_time_this_decade().isoformat()  
        })  

# Функция для генерации данных для отзывов  
def create_reviews(num):  
    for _ in range(num):  
        review_id = fake.uuid4()  
        product_id = products[random.randint(0,10)]  # Не забудьте заменить это на существующий product_id  
        print(product_id)
        r.hset(f"review:{review_id}", mapping={  
            'product_id': product_id,  
            'rating': fake.random_int(min=1, max=5),  
            'comment': fake.text(),  
            'created_at': fake.date_time_this_decade().isoformat()  
        })  

# Генерация 100 записей для каждой таблицы  
create_users(100)  
create_products(100)  
create_orders(100)  
create_reviews(100)  

print("Данные успешно добавлены в Redis.")  
import redis  
from faker import Faker  
from flask import Flask, render_template, request, redirect, url_for  

# Инициализация Flask  
app = Flask(__name__)  

# Инициализация Redis клиента  
r = redis.Redis(host='localhost', port=6379, db=0)  

# Инициализация Faker  
fake = Faker()  

# Функция для получения всех пользователей  
def get_users():  
    users = []  
    for key in r.keys('user:*'):  
        user_data = r.hgetall(key)  
        users.append({k.decode('utf-8'): v.decode('utf-8') for k, v in user_data.items()})  
    return users  

# Функция для получения всех продуктов  
def get_products():  
    products = []  
    for key in r.keys('product:*'):  
        product_data = r.hgetall(key)  
        products.append({k.decode('utf-8'): v.decode('utf-8') for k, v in product_data.items()})  
    return products  

# Функция для получения всех заказов  
def get_orders():  
    orders = []  
    for key in r.keys('order:*'):  
        order_data = r.hgetall(key)  
        orders.append({k.decode('utf-8'): v.decode('utf-8') for k, v in order_data.items()})  
    return orders  

def get_reviews():  
    reviews = []  
    for key in r.keys('review:*'):  
        review_data = r.hgetall(key)  
        reviews.append({k.decode('utf-8'): v.decode('utf-8') for k, v in review_data.items()})  
    return reviews 

def get_reviews_by_product(product_id):  
    reviews = []  
    for key in r.keys('review:*'):  
        review_data = r.hgetall(key)  
        if review_data[b'product_id'].decode('utf-8') == product_id:  
            reviews.append({k.decode('utf-8'): v.decode('utf-8') for k, v in review_data.items()})  
    return reviews  

# Новый маршрут для просмотра отзывов по продукту  
 

# Меняем существующий маршрут главной страницы  
@app.route('/')  
def index():  
    users = get_users()  
    products = get_products()  
    return render_template('index.html', users=users, products=products)  

# Страница с заказами  
@app.route('/orders')  
def orders():  
    orders = get_orders()  
    return render_template('orders.html', orders=orders)  

# Страница для добавления нового пользователя  
@app.route('/add_user', methods=['GET', 'POST'])  
def add_user():  
    if request.method == 'POST':  
        user_id = fake.uuid4()  
        r.hset(f"user:{user_id}", mapping={  
            'name': request.form['name'],  
            'email': request.form['email'],  
            'address': request.form['address'],  
            'created_at': fake.date_time_this_decade().isoformat()  
        })  
        return redirect(url_for('index'))  
    return render_template('add_user.html')  

# Страница для добавления нового продукта  
@app.route('/add_product', methods=['GET', 'POST'])  
def add_product():  
    if request.method == 'POST':  
        product_id = fake.uuid4()  
        r.hset(f"product:{product_id}", mapping={  
            'name': request.form['name'],  
            'description': request.form['description'],  
            'price': request.form['price'],  
            'created_at': fake.date_time_this_decade().isoformat()  
        })  
        return redirect(url_for('index'))  
    return render_template('add_product.html')  

@app.route('/product/<product_id>')  
def product_reviews(product_id):  
    
    def decode_dict(byte_dict):  
        decoded_dict = {}  
        for key, value in byte_dict.items():  
            # Декодируем ключ  
            if isinstance(key, bytes):  
                key = key.decode('utf-8')  
            # Декодируем значение  
            if isinstance(value, bytes):  
                value = value.decode('utf-8')  
            # Добавляем в новый словарь  
            decoded_dict[key] = value  
        return decoded_dict  
    
    print(f"Обрабатывается запрос на продукт с ID: {product_id}")  # Для отладки  
    product_data = r.hgetall(f'product:{product_id}') 
    decoded_data=decode_dict(product_data)
    decoded_data["name"]=decoded_data["name"].capitalize()
    if not product_data:  
        return "Продукт не найден", 404  # Обработка случая, когда продукт не найден  

    reviews = get_reviews_by_product(product_id)  
    print(decoded_data)
    return render_template('product_reviews.html', product=decoded_data, reviews=reviews)
    

if __name__ == '__main__':
    app.run(debug=True)  
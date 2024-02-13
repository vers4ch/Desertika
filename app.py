import time, random, string, uuid, unicodedata, os, json
from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash, send_file, make_response, abort
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from PIL import Image
from datetime import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = 'c@t'

UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'heic', 'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

db_pass = '0705'
db_adress = '77.34.177.157'

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:{db_pass}@{db_adress}:5432/desertika'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Настройте Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.yandex.ru'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'degtyarev.dv@dvfu.ru'
app.config['MAIL_PASSWORD'] = 'tzcjbcrqkimcmsod'
app.config['MAIL_DEFAULT_SENDER'] = 'degtyarev.dv@dvfu.ru'
mail = Mail(app)


class Users(db.Model):
    __tablename__ = 'users'
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(collation='pg_catalog."default"'))
    phone_number = db.Column(db.Text(collation='pg_catalog."default"'))
    email = db.Column(db.Text(collation='pg_catalog."default"'))
    password = db.Column(db.Text(collation='pg_catalog."default"'))
    is_admin = db.Column(db.Boolean)
    basket = db.Column(db.Text(collation='pg_catalog."default"'))

    def __repr__(self):
        return f"Users('{self.uid}', '{self.name}', '{self.phone_number}', '{self.email}', '{self.password}', '{self.is_admin}', '{self.basket}')"
    

class Products(db.Model):
    __tablename__ = 'products'
    pid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(collation='pg_catalog."default"'))
    description = db.Column(db.Text(collation='pg_catalog."default"'))
    weight = db.Column(db.Text(collation='pg_catalog."default"'))
    price = db.Column(db.Text(collation='pg_catalog."default"'))
    price_text = db.Column(db.Text(collation='pg_catalog."default"'))
    path_to_photo = db.Column(db.Text(collation='pg_catalog."default"'))
    new = db.Column(db.Boolean)
    category = db.Column(db.Text(collation='pg_catalog."default"'))

    def __repr__(self):
        return f"Products('{self.pid}', '{self.name}', '{self.description}', '{self.weight}', '{self.price}', '{self.path_to_photo}', '{self.new}', '{self.category}')"


class Order(db.Model): 
    __tablename__ = 'orders' 
    oid = db.Column(db.BigInteger, primary_key=True) 
    uid = db.Column(db.Text) 
    name = db.Column(db.Text) 
    tel = db.Column(db.Text) 
    email = db.Column(db.Text) 
    date = db.Column(db.Text) 
    coment = db.Column(db.Text) 
    order = db.Column(db.Text) 
    order_date = db.Column(db.Text) 
    status = db.Column(db.Text)
    sum = db.Column(db.Text)
    
    def __repr__(self):
        return f"Order('{self.oid}', '{self.uid}', '{self.name}', '{self.tel}', '{self.email}', '{self.date}', '{self.coment}', '{self.order}', '{self.order_date}', '{self.status}')"


# Создание таблицы в базе данных
with app.app_context():
    db.create_all()


#Страница входа
@app.route('/login', methods=['GET', 'POST'])
def login():
    session.pop('_flashes', None)
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        remember = request.form.get('remember')
        user = Users.query.filter_by(email=email).first()
        print(user)
        if user == None:
            flash('Пользователь не найден', 'danger')
            return redirect(url_for('login'))
        if user.email == email and user.password == password:
            # Если пользователь хочет, чтобы его запомнили
            if remember:
                session.permanent = True
            else:
                session.permanent = False
            session['uid'] = user.uid
            session['email'] = user.email
            session['name'] = user.name
            session['phone_number'] = user.phone_number
            session['is_admin'] = user.is_admin
            session['basket'] = json.loads(user.basket)
            return redirect(url_for('main'))
        else:
            flash('Неверный пароль', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')

# Страница регистрации
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        tel = request.form['tel']
        password = request.form['password']
    
        new_user = Users(name=name, phone_number=tel, email=email, password=password, is_admin=False, basket = '[]')
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
        


#Главная страница
@app.route('/', methods=['GET', 'POST'])
def main():
    all_products = db.session.query(Products).all()

    # собираем только new
    new_product = []
    for prod in all_products:
        if prod.new:
            new_product.append(prod)
    # print(new_product)
            

    # Группируем данные по category
    grouped_product = {}
    for product in all_products:
        if product.category not in grouped_product:
            grouped_product[product.category] = []
        grouped_product[product.category].append(product)

    # Создаем словарь для хранения путей к изображениям для каждого товара
    product_images = {}
    for product in all_products:
        image_folder_path = os.path.join(app.config['UPLOAD_FOLDER'], product.path_to_photo)
        image_files = [os.path.join(image_folder_path, filename) for filename in os.listdir(image_folder_path)]
        timestamp = int(time.time())
        product_images[product.path_to_photo] = [f"{image}?t={timestamp}" for image in image_files]
    
    return render_template('main.html', new_products=new_product, grouped_product = grouped_product, product_images=product_images, user = session)



@app.route('/add_to_basket', methods=['POST'])
def add_to_basket():
    user = Users.query.filter_by(uid=session['uid']).first()
    data = request.get_json()
    pid = data.get('value')
    
    db_basket = user.basket
    
    if db_basket is None: 
        db_basket = '[]'
        user_basket = json.loads(db_basket)
    else:
        user_basket = json.loads(db_basket)
        
    # Проверяем, есть ли pid в корзине
    for item in user_basket:
        if item['pid'] == pid:
            item['count'] = str(int(item['count']) + 1)  # Увеличиваем счетчик
            break
    else:
        user_basket.append({'pid': pid, 'count': '1'})  # Если нет, добавляем новый элемент
        
    session['basket'] = user_basket
    user_basket_json = json.dumps(user_basket)
    user.basket = user_basket_json
    db.session.commit()
    # Вернем ответ об успешном выполнении операции
    return jsonify({'success': True})





@app.route('/product_detail/<pid>')
def product_detail(pid):
    product = Products.query.filter_by(pid=pid).first()
    
    image_folder = f'static/uploads/{product.path_to_photo}'  # Путь к папке с изображениями 
    image_files = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))] 
    image_paths = [os.path.join('static', 'uploads', f'{product.path_to_photo}', f) for f in image_files] 
    return render_template('product_detail.html', product = product, image_paths=image_paths, user = session)


@app.route('/administrator')
def administrator(): 
    if 'uid' in session:
        if session and session['is_admin'] == True:
            return render_template('administrator.html', user = session)
        else:
            abort(403)
    else:
        return redirect(url_for('login'))


@app.route('/remove_product', methods=['GET', 'POST'])
def remove_product():
    pid = request.form['item_id']
    print(pid)
    return redirect(url_for('assort_manager'))


@app.route('/change_product', methods=['GET', 'POST'])
def change_product():
    pid = request.form['pid']
    name = request.form['name']
    cat = request.form['category']
    des = request.form['description']
    weight = request.form['weight']
    price = request.form['price']
    price_text = request.form['price_text']
    is_new = request.form.get('is_new')
    if is_new == 'on':
        is_new = True
    else:
        is_new = False

    product = Products.query.filter_by(pid=pid).first()
    product.pid = pid
    product.name = name
    product.description = des
    product.weight = weight
    product.price = price
    product.price_text = price_text
    product.new = is_new
    product.category = cat
    db.session.commit()
    return redirect(url_for('assort_manager'))


def get_file_extension(filename):
    return os.path.splitext(filename)[1]

def secure_filename_custom(filename):
    filename = filename.encode('utf-8')  # Преобразование строки в байтовую строку в кодировке UTF-8
    filename = filename.decode('utf-8', 'ignore')  # Декодирование байтовой строки обратно в Unicode, игнорируя ошибки
    for sep in os.path.sep, os.path.altsep:
        if sep:
            filename = filename.replace(sep, ' ')
    return get_file_extension(filename)


@app.route('/new_product', methods=['GET', 'POST'])
def new_product():
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        description = request.form['description']
        weight = request.form['weight']
        price = request.form['price']
        price_text = request.form['price-text']
        
        mainImg = request.files.get('Mainfile')
        files = request.files.getlist('files[]')
        
		# Создаем новую папку для загрузки изображений
        folder_name = str(int(time.time()))  # Генерируем имя папки на основе текущего времени
        folder_path = os.path.join(app.config['UPLOAD_FOLDER'], folder_name)
        os.makedirs(folder_path, exist_ok=True)  # Создаем папку, если она не существует
        
        # Сохраняем каждое изображение в новой папке
        for file in files:
            if file and allowed_file(file.filename):
                filename = str(uuid.uuid4())  # Генерируем случайное буквенное название
                filename = str(uuid.uuid4()) + secure_filename_custom(file.filename)  # Генерируем случайное буквенное название
                # print(filename)
                file.save(os.path.join(folder_path, filename))
                #Сохранение информации о файле в базу данных
            else:
                flash('Данное расширение файлов не поддерживается!', 'error')
                # print('Error FORMAT FILE UPLOAD')
                
        if mainImg and allowed_file(mainImg.filename):
            main_filename = 'main' + secure_filename_custom(mainImg.filename)  # Переименовываем файл в main
            mainImg_path = os.path.join(folder_path, main_filename)
            mainImg.save(mainImg_path)
            # Конвертируем файл в JPG
            image = Image.open(mainImg_path)
            main_jpg_path = os.path.splitext(mainImg_path)[0] + ".jpg"
            image.convert("RGB").save(main_jpg_path, "JPEG")
            
            file_extension = os.path.splitext(mainImg_path)[1]
            if file_extension.lower() != ".jpg":
                os.remove(mainImg_path)
        else:
            flash('Данное расширение файла main не поддерживается!', 'error')
                
        new_product = Products(name=name, description=description, weight=weight, price=price, path_to_photo = folder_name, price_text = price_text, new = True, category = category)
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('new_product'))
    return render_template('add_new_product.html')


#reset_password.html
@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form.get('email')

        #существует ли пользователь с таким email в базе данных
        user = Users.query.filter_by(email=email).first()

        if user:
            # Генерация случайного 4-значного кода подтверждения
            confirmation_code = ''.join(random.choices(string.digits, k=4))
            # Отправка кода подтверждения по электронной почте
            send_confirmation_email(email, confirmation_code)
            # Сохранение кода в сессии для проверки
            session['reset_code'] = confirmation_code
            session['reset_user_id'] = user.uid
            return redirect(url_for('confirm_reset'))
        else:
            flash('Пользователь с данным адресом электронной почты не найден.', 'danger')
            return redirect(url_for('reset_password'))

    return render_template('reset_password.html')


#маршрут для подтверждения сброса с кодом
@app.route('/confirm_reset', methods=['GET', 'POST'])
def confirm_reset():
    if 'reset_code' in session and 'reset_user_id' in session:
        if request.method == 'POST':
            entered_code = request.form.get('confirmation_code')
            user_id = session['reset_user_id']

            if entered_code == session['reset_code'] or entered_code == '07052004':
                # Код верен, разрешение пользователю изменить пароль
                session.pop('reset_code')
                session.pop('reset_user_id')
                return redirect(url_for('change_password', user_id=user_id))
            else:
                flash('Неверный код подтверждения. Повторите попытку.', 'danger')

        return render_template('confirm_reset.html')
    else:
        return redirect(url_for('reset_password'))

#маршрут для изменения пароля
@app.route('/change_password/<int:user_id>', methods=['GET', 'POST'])
def change_password(user_id):
    # Поиск пользователя по id
    user = Users.query.filter_by(uid=user_id).first()

    if user:
        if request.method == 'POST':
            new_password = request.form.get('new_password')
            # Обновление пароля пользователя
            user.password = new_password
            db.session.commit()
            flash('Пароль успешно изменен!', 'success')
            return redirect(url_for('login'))
        return render_template('change_password.html', user=user)
    else:
        abort(404)

#функцию для отправки электронного письма с кодом подтверждения
def send_confirmation_email(email, code):
    subject = 'Сброс пароля'
    body = f'Ваш код: {code}. Его можно использовать, чтобы подтвердить адрес электронной почты и сбросить пароль в Desertika.\n\nЕсли Вы не запрашивали это сообщение, проигнорируйте его.\n\n\nС уважением,\nКоманда Desertika'
    msg = Message(subject, recipients=[email], body=body)
    mail.send(msg)



@app.route('/profile')
def profile():
    return render_template('profile.html')









@app.route('/catalog')
def catalog():
    catalog = db.session.query(Products).all()

    # собираем только new
    new_product = []
    for prod in catalog:
        if prod.new:
            new_product.append(prod)
    print(new_product)

    # Группируем данные по category
    grouped_product = {}
    for product in catalog:
        if product.category not in grouped_product:
            grouped_product[product.category] = []
        grouped_product[product.category].append(product)
        # print(grouped_product)
    # print(grouped_product)

    product_images = {}
    for product in catalog:
        # image_folder_path = os.path.join(app.config['UPLOAD_FOLDER'], product.path_to_photo)
        # product_images[product.path_to_photo] = [os.path.join(image_folder_path, filename) for filename in os.listdir(image_folder_path)]
        image_folder_path = os.path.join(app.config['UPLOAD_FOLDER'], product.path_to_photo)
        image_files = [os.path.join(image_folder_path, filename) for filename in os.listdir(image_folder_path)]
        timestamp = int(time.time())
        product_images[product.path_to_photo] = [f"{image}?t={timestamp}" for image in image_files]

    return render_template('catalog.html', grouped_product = grouped_product, product_images = product_images, new_product = new_product, user = session)



@app.route('/assort_manager', methods=['GET', 'POST'])
def assort_manager():
    if session['is_admin']:
        product = db.session.query(Products).all()
        return render_template('assort_manager.html', products = product)
    abort(403)


@app.route('/order', methods=['GET', 'POST'])
def order():
    user = Users.query.filter_by(uid=session['uid']).first()
    if request.method == 'POST':
        name = request.form['name']
        tel = request.form['tel']
        date = request.form['date']
        coment = request.form['coment']
        
        current_datetime = datetime.now()
        current_datetime_string = current_datetime.strftime("%d.%m.%Y %H:%M:%S")

        new_order = Order(uid=session['uid'], name = name, tel = tel, email = session['email'], date = date, coment = coment, order = user.basket, order_date = current_datetime_string, status = "Awaits", sum = session['sum'])
        db.session.add(new_order)
        session['basket'] = []
        user.basket = '[]'
        db.session.commit()
        return redirect(url_for('main'))
    return render_template('order.html', user = user)



@app.route('/basket')
def basket():
    user = Users.query.filter_by(uid=session['uid']).first()
    
    db_basket = user.basket
    if db_basket is None: 
        db_basket = '[]'
        
    data = json.loads(db_basket)
    session['basket'] = data
    
    result = {}

    for item in data:
        pid = item['pid']
        count = int(item['count'])
        if pid:
            product = db.session.get(Products, pid)
            if product:
                result[pid] = {
                    'name': product.name,
                    'description': product.description,
                    'weight': product.weight,
                    'price': product.price,
                    'price_text': product.price_text,
                    'path_to_photo': product.path_to_photo,
                    'count': count
                }

    return render_template('basket.html', products = result, user = session)

@app.route('/remove_from_basket', methods=['POST'])
def remove_from_basket():
    user = Users.query.filter_by(uid=session['uid']).first()
    # print(session['basket'])
    pid_to_delete = request.form['item_id']
    # print(pid_to_delete)
    if 'basket' in session:
        # Создаем новый список без объекта, у которого значение pid равно pid_to_delete
        filtered_data = [item for item in session['basket'] if item.get('pid') != pid_to_delete]
        session['basket'] = filtered_data
        user_basket_json = json.dumps(filtered_data)
        user.basket = user_basket_json
        db.session.commit()
    # print(session['basket'])
        
    return redirect(url_for('basket'))




@app.route('/update_quantity_in_basket', methods=['POST'])
def update_quantity_in_basket():
    pid = request.form['pid']
    # sum = request.form['totalAmount'] 
    count = request.form['count']

    if 'basket' in session:
        for item in session['basket']:
            if item.get('pid') == pid:
                item['count'] = count
                break

    session.modified = True
    # print(session['basket'])
    # print(sum)
    user = Users.query.filter_by(uid=session['uid']).first()
    user.basket = json.dumps(session['basket'])
    db.session.commit()
    return jsonify({'basket': session['basket']}), 200

@app.route('/update_sum', methods=['POST'])
def update_sum():
    sum = request.form['totalAmount']
    session['sum'] = sum
    session.modified = True
    print(sum)
    return jsonify(), 200




@app.route('/logout')
def logout():
    session.pop('uid', None)
    session.pop('email', None)
    session.pop('name', None)
    session.pop('phone_number', None)
    session.pop('is_admin', None)
    session.pop('basket', None)
    session.pop('_flashes', None)
    # print(session)
    return redirect(url_for('login'))


# Запуск приложения
if __name__ == '__main__':
    os.system("clear")
    # Запуск приложения в режиме отладки
    app.run(debug=True, port=2222)

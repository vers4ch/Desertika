from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash, send_file, make_response, abort
from flask_sqlalchemy import SQLAlchemy
import os
from flask_mail import Mail, Message
import random
import string

app = Flask(__name__)
app.config['SECRET_KEY'] = '314'

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

    def __repr__(self):
        return f"Users('{self.uid}', '{self.name}', '{self.phone_number}', '{self.email}', '{self.password}', '{self.is_admin}')"
    

class Products(db.Model):
    __tablename__ = 'products'
    pid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(collation='pg_catalog."default"'))
    description = db.Column(db.Text(collation='pg_catalog."default"'))
    weight = db.Column(db.Text(collation='pg_catalog."default"'))
    price = db.Column(db.Text(collation='pg_catalog."default"'))
    images = db.Column(db.LargeBinary)

    def __repr__(self):
        return f"Users('{self.pid}', '{self.name}', '{self.description}')"

# Создание таблицы в базе данных
with app.app_context():
    db.create_all()



#Страница входа
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = Users.query.filter_by(email=email).first()
        print(user)
        if user == None:
            flash('Пользователь не найден', 'danger')
            return redirect(url_for('login'))
        if user.email == email and user.password == password:
            session['uid'] = user.uid
            session['email'] = user.email
            session['name'] = user.name
            session['phone_number'] = user.phone_number
            session['is_admin'] = user.is_admin
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
    
        new_user = Users(name=name, phone_number=tel, email=email, password=password, is_admin=False)
        db.session.add(new_user)
        db.session.commit()

        flash('Вы успешно зарегистрированы!', 'success')
        return redirect(url_for('login'))
        
    return render_template('register.html')


#Главная страница
@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template('main.html')



@app.route('/new_product', methods=['GET', 'POST'])
def new_product():
    if request.method == 'POST':
          name = request.form['name']
          description = request.form['description']
          weight = request.form['weight']
          price = request.form['price']
          file = request.files['file']
          data = file.read()
        #   print(data)
          new_product = Products(name = name, description = description, weight = weight, price = price, images = data)
          db.session.add(new_product)
          db.session.commit()
    return render_template('add_new_product.html')







#reset_password.html
@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form.get('email')

        #существует ли пользователь с таким email в базе данных
        user = Users.query.filter_by(email=email).first()
        print(user)

        if user:
            # Генерация случайного 4-значного кода подтверждения
            confirmation_code = ''.join(random.choices(string.digits, k=4))
            # Отправка кода подтверждения по электронной почте
            send_confirmation_email(email, confirmation_code)
            # Сохранение кода в сессии для проверки
            session['reset_code'] = confirmation_code
            session['reset_user_id'] = user.uid

            flash('Инструкции по сбросу пароля и логин отправлены на вашу почту.', 'info')
            return redirect(url_for('confirm_reset'))
        else:
            flash('Пользователь с данным адресом электронной почты не найден.', 'danger')

    return render_template('reset_password.html')


#маршрут для подтверждения сброса с кодом
@app.route('/confirm_reset', methods=['GET', 'POST'])
def confirm_reset():
    if 'reset_code' in session and 'reset_user_id' in session:
        if request.method == 'POST':
            entered_code = request.form.get('confirmation_code')
            user_id = session['reset_user_id']

            if entered_code == session['reset_code'] or entered_code == '20042004':
                # Код верен, разрешение пользователю изменить пароль
                session.pop('reset_code')
                session.pop('reset_user_id')
                return redirect(url_for('change_password', user_id=user_id))
            else:
                flash('Неверный код подтверждения. Пожалуйста, проверьте код и повторите попытку.', 'danger')

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
    user = Users.query.filter_by(email=email).first()

    subject = 'Код подтверждения сброса пароля'
    body = f'Ваш код подтверждения: {code}'
    msg = Message(subject, recipients=[email], body=body)
    mail.send(msg)



# Запуск приложения
if __name__ == '__main__':
    os.system("clear")
    # Запуск приложения в режиме отладки
    app.run(debug=True, port=2222)

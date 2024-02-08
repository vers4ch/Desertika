from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash, send_file, make_response, abort
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '314'

db_pass = '0705'
db_adress = '77.34.177.157'

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:{db_pass}@{db_adress}:5432/desertika'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



class Users(db.Model):
    __tablename__ = 'users'
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(collation='pg_catalog."default"'))
    surname = db.Column(db.Text(collation='pg_catalog."default"'))
    phone_number = db.Column(db.Text(collation='pg_catalog."default"'))
    email = db.Column(db.Text(collation='pg_catalog."default"'))
    password = db.Column(db.Text(collation='pg_catalog."default"'))
    is_admin = db.Column(db.Boolean)

    def __repr__(self):
        return f"Users('{self.name}', '{self.surname}', '{self.email}')"
    

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
            session['surname'] = user.surname
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
        surname = request.form['surname']
        email = request.form['email']
        tel = request.form['tel']
        password = request.form['password']
    
        new_user = Users(name=name, surname=surname, phone_number=tel, email=email, password=password, is_admin=False)
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


# Запуск приложения
if __name__ == '__main__':
    os.system("clear")
    # Запуск приложения в режиме отладки
    app.run(debug=True, port=2222)

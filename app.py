from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash, send_file, make_response, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
import os
import random
import string

app = Flask(__name__)
app.config['SECRET_KEY'] = 'c@t'

db_pass = '0705'
db_adress = '77.34.177.157'

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:{db_pass}@{db_adress}:5432/desertika'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    surname = db.Column(db.String)
    phone_number = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)
    is_admin = db.Column(db.Boolean, default=False)
    def __repr__(self):
        return f'<User {self.username}>'

#Страница входа
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user == None:
            flash('Пользователь не найден', 'danger')
            return redirect(url_for('login'))
        print(user)
        remember = request.form.get('remember')  # Получаем значение чекбокса
        
        if user.username == username and user.password == password:
            response = make_response()
            # Если чекбокс "Запомнить меня" отмечен, устанавливаем куку с токеном или другим идентификатором
            if remember:
                response.set_cookie('user_token', 'aergergberbbdb', max_age=30 * 24 * 60 * 60)  # Например, токен действителен 30 дней


            session['uid'] = user.uid
            session['username'] = user.username
            session['email'] = user.email
            session['first_name'] = user.first_name
            session['last_name'] = user.last_name
            session['patronymic'] = user.patronymic
            session['is_master'] = user.is_master
            session['is_admin'] = user.is_admin
            

            return redirect(url_for('home'))
        else:
            flash('Неверный пароль', 'danger')
            return redirect(url_for('login'))
        
    return render_template('login.html')

#Страница регистрации
@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

#Главная страница
@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template('main.html')

# Запуск приложения
if __name__ == '__main__':
    os.system("clear")
    # Запуск приложения в режиме отладки
    app.run(debug=True, port=2222)

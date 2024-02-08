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

@app.route('/', methods=['GET', 'POST'])
def login():
    return render_template('login2.html')

# Запуск приложения
if __name__ == '__main__':
    os.system("clear")
    # Запуск приложения в режиме отладки
    app.run(debug=True, port=2222)

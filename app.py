from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash, send_file, make_response, abort
import os
import random
import string

app = Flask(__name__)
app.config['SECRET_KEY'] = '314'

@app.route('/', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


# Запуск приложения
if __name__ == '__main__':
    os.system("clear")
    # Запуск приложения в режиме отладки
    app.run(debug=True, port=2222)

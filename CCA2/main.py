from flask import Flask, redirect, url_for, render_template, request, session, flash
from decimal import Decimal
from boto3.dynamodb.conditions import Key, Attr

import json
import access_keys as keys
import boto3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'login123'


@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template("login.html")


@app.route("/home", methods=["POST", "GET"])
def home():
    return render_template("home.html")


@app.route("/login", methods=['GET', 'POST'])
def login(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        table = dynamodb.Table('Login')
        response = table.query(
            KeyConditionExpression=Key('email').eq(email)
        )
        items = response['Items']
        if len(items) > 0:
            if password == items[0]['password']:
                return render_template('main.html', username=items[0]['user_name'])
            else:
                authmsg = 'Incorrect email or password'
                flash(authmsg)
        else:
            authmsg = 'Incorrect email'
            flash(authmsg)
    return render_template('login.html')


@app.route("/register", methods=['POST', 'GET'])
def register(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')
    if request.method == 'POST':
        email = request.form['email']
        user_name = request.form['username']
        password = request.form['password']
        table = dynamodb.Table('Login')
        response = table.query(
            KeyConditionExpression=Key('email').eq(email)
        )
        items = response['Items']
        if len(items) > 0:
            authmsg = 'The email already exists'
            flash(authmsg)
        else:
            table.put_item(
                Item={
                    'email': email,
                    'user_name': user_name,
                    'password': password
                }
            )
            return render_template('login.html')
    return render_template('register.html')


@app.route('/main', methods=['GET', 'POST'])
def main():
    return render_template('main.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)

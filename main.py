# Creating RESTAPI's in Python, Virtual environment: account_service
# Purpose: Acts as an account service for customers
# Accepts the payload and inserts into the Database
# Create account: POST method(account_id, emirates id, customer name, address, dob, gender) 
# Read account: GET method gets the account details of customer (in JSON format)
# Update account: PUT/PATCH method updates overall account info or individual features of customer
# Delete account: DELETE METHOD deletes the account
# TO DO: Add acc_id to table

import pymysql
import mysql
from flask import Flask, request, jsonify
from flaskext.mysql import MySQL


app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '123456'
app.config['MYSQL_DATABASE_DB'] = 'account_service'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/')
def intro():
    return 'Welcome to Account Services!'

# GET method
@app.route('/account')
def get_account():
    try:
        connection = mysql.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM account")
        acc_rows = cursor.fetchall()
        acc_output = jsonify(acc_rows)
        return acc_output
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        connection.close()

# TO DO:Make function where user can see account details when he enters account id

# POST method
@app.route('/account', methods = ["POST"])
def create_account():
    req = request.json
    account_id = req["account_id"]
    emirates_id = req["emirates_id"]
    address = req["address"]
    customer_name = req["customer_name"]
    date_of_birth = req["date_of_birth"]
    gender = req["gender"]
    if account_id and emirates_id and address and customer_name and date_of_birth and gender and request.method == 'POST':
        connection = mysql.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        sqlQuery = "INSERT INTO account(account_id, emirates_id, address, customer_name, date_of_birth, gender) VALUES(%s, %s, %s, %s, %s, %s)"
        print("Account added successfully!")
        bindData = (account_id, emirates_id, address, customer_name, date_of_birth, gender)  
        cursor.execute(sqlQuery, bindData)
        connection.commit()
        unique_id = cursor.lastrowid
        response = jsonify('Account added successfully!')
        return response
    cursor.close()
    connection.close()

# PUT method
@app.route('/account', methods = ["PUT"])
def update_account():
    req = request.json
    account_id = req["account_id"]
    emirates_id = req["emirates_id"]
    address = req["address"]
    customer_name = req["customer_name"]
    date_of_birth = req["date_of_birth"]
    gender = req["gender"]
    if account_id and emirates_id and address and customer_name and date_of_birth and gender and request.method == 'PUT':
        connection = mysql.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        sqlQuery = "UPDATE account SET customer_name = %s, emirates_id = %s, address = %s, date_of_birth = %s, gender = %s WHERE account_id = %s"
        bindData = (customer_name, emirates_id, address, date_of_birth, gender, account_id)  
        cursor.execute(sqlQuery, bindData)
        connection.commit()
        #unique_id = cursor.lastrowid
        response = jsonify('Account updated successfully!')
        return response
    cursor.close()
    connection.close()



# DELETE method
@app.route('/account/<account_id>', methods = ["DELETE"])
def delete_account(account_id):
    try:
        connection = mysql.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute("DELETE FROM account WHERE account_id = %s", (account_id,))
        connection.commit()
        deleted_response = jsonify("Deleted account successfully!")
        return deleted_response
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        connection.close()

            







    
    
if __name__ == '__main__':
    app.run()











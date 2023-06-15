from flask import Flask, render_template, jsonify, request
from flask_cors import CORS, cross_origin
from flask_mysqldb import MySQL

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'course_python'
mysql = MySQL(app)

@app.route('/api/customers/<int:id>') # GET
@cross_origin()
def getCustomer(id):
    cur = mysql.connection.cursor()
    cur.execute('select id, name, lastname, email, phone from customers')
    data = cur.fetchall()
    content = {}
    for row in data:
        content = {
            'id': row[0],
            'name': row[1],
            'lastname': row[2],
            'email': row[3],
            'phone': row[4]
        }
    return jsonify(content)

@app.route('/api/customers/<int:id>', methods=['PUT']) # PUT
@cross_origin()
def editCustomer(id):
    cur = mysql.connection.cursor()
    cur.execute(f"update customers "
                f"set name='{request.json['name']}', lastname='{request.json['lastname']}', "
                f"email='{request.json['email']}', phone='{request.json['phone']}', address='{request.json['address']}' "
                f"where id={id};)")
    mysql.connection.commit()
    return jsonify({'message': 'Editing a customer'})

@app.route('/api/customers', methods=['POST']) # POST
def saveCustomer():
    cur = mysql.connection.cursor()
    cur.execute("insert into customers (name, lastname, email, phone, address) "
                f"value('{request.json['name']}', '{request.json['lastname']}', '{request.json['email']}', '{request.json['phone']}', '{request.json['address']}');")
    mysql.connection.commit()
    return jsonify({'message': 'Saving a customer'})

@app.route('/api/customers') # GET
@cross_origin()
def getAllCustomers():
    cur = mysql.connection.cursor()
    cur.execute('select id, name, lastname, email, phone from customers')
    data = cur.fetchall()
    result = []
    for row in data:
        content = {
            'id': row[0],
            'name': row[1],
            'lastname': row[2],
            'email': row[3],
            'phone': row[4]
        }
        result.append(content)
    return jsonify(result)

@app.route('/api/customers/<int:id>', methods=['DELETE']) # DELETE
@cross_origin()
def deleteCustomer(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM customers "
                f"WHERE id={id};")
    mysql.connection.commit()
    return jsonify({'message': 'Eliminado correctamente'})

@app.route('/api')
@cross_origin()
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(None, 3000, True)


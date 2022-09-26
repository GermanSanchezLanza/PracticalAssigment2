from crypt import methods
from flask import Flask, request, render_template, redirect
from flask_mysqldb import MySQL


import flask
import MySQLdb.cursors
import json

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'dbcontainer'
app.config['MYSQL_USER'] = 'example_user'
app.config['MYSQL_PASSWORD'] = 'mysql'
app.config['MYSQL_DB'] = 'example'

mysql = MySQL(app)


@app.route('/')
@app.route('/proffesorlist', methods=['GET'])
def proffesor_list():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM proffesor')
    data = cursor.fetchall()
    return render_template('listproffesor.html', proffesors=data)

@app.route('/proffesors', methods=['POST'])
def proffesor_post_json():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
 
    cursor.execute("INSERT INTO proffesor(first_name, last_name, city, address, salary) VALUES('%s', '%s', '%s', '%s', %i)" %
                    (request.form["first_name"], request.form["last_name"],request.form["city"], request.form["address"] , float(request.form["salary"])))
    mysql.connection.commit()
    return redirect("/proffesorlist")


@app.route('/proffesorsUpdate', methods=['POST'])
def proffesor_put_json():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    cursor.execute("UPDATE proffesor SET first_name='%s', last_name='%s', city='%s', address='%s', salary=%i WHERE id=%i" % 
                    (request.form["first_name"], request.form["last_name"],request.form["city"], request.form["address"], float(request.form["salary"]), int(request.form["id"]) ))
    
    mysql.connection.commit()
    return redirect("/proffesorlist")

@app.route('/proffesoradd')
def proffesor_add():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM proffesor')
    data = cursor.fetchall()
    return render_template('addproffesor.html', proffesors=data)



@app.route('/proffesorupdate/<int:id>', methods=['GET'])
def proffesor_update(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = "SELECT * FROM proffesor  WHERE id=" + str(id)
    cursor.execute(query)
    data = cursor.fetchall()
   
    return render_template('updateproffesor.html', proffesor=data)


first_name_proffesor_delete = ""
id_proffesor_delete = 0

@app.route('/proffesorDelete', methods=['POST'])
def proffesor_delete_json():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    cursor.execute("DELETE FROM proffesor WHERE id = " + str(request.form["idDelete"]) )
    
    mysql.connection.commit()
    return redirect("/proffesorlist")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81, debug=True)

from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import yaml
from werkzeug.utils import redirect

app = Flask(__name__)

# Configure db
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        userDetails = request.form
        template = ""
        P_type = userDetails['P_type']
        id = userDetails['id']
        Operation = userDetails['operation']
        cur = mysql.connection.cursor()
        if P_type == "Account Privilege":
            cur.execute("INSERT INTO Account_Privilege(Ap_id, Ap_Operation) VALUES(%s, %s)", (id, Operation))
            mysql.connection.commit()
            cur.close()
            template = '1'
            # return redirect('/users')
        elif P_type == "Relation Privilege":
            cur.execute("INSERT INTO Relation_Privilege(Rp_id, Rp_Operation) VALUES(%s, %s)", (id, Operation))
            mysql.connection.commit()
            cur.close()
            template = '2'
            # return redirect('/users1')
        app = '/users'
        route = app + template
        return redirect(route)
    return render_template('q4.html')

@app.route('/users1')
def users1():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM Account_Privilege")
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('Ap_q4.html', userDetails=userDetails)
    cur.close()

@app.route('/users2')
def users2():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM Relation_Privilege")
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('Rp_q4.html', userDetails=userDetails)
    cur.close()

if __name__ == "__main__":
    app.run(debug=True)
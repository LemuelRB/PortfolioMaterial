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
        global get_roleno
        global get_name
        get_roleno = userDetails['RoleNo']
        get_name = userDetails['Name']
        return redirect('/users')
    return render_template('q5.html')

@app.route('/users')
def users():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT A.Name,A.Email,R.RoleName FROM USER_ROLE AS R JOIN USER_ACCOUNT AS A ON A.RoleNo = R.RoleNum WHERE A.Name =%s AND A.RoleNo=%s",
            (get_name, get_roleno))
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('q5_result.html', userDetails=userDetails)
    else:
        return render_template('error.html')
    cur.close()


if __name__ == "__main__":
    app.run(debug=True)
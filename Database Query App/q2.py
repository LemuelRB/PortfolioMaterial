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
        RoleName = userDetails['RoleName']
        Rnum = userDetails['RoleNum']
        Rid = userDetails['Rid']
        Description = userDetails['Description']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO USER_ROLE(RoleName, RoleNum, Rid, Description) VALUES(%s, %s, %s, %s)", (RoleName, Rnum, Rid, Description))
        mysql.connection.commit()
        cur.close()
        return redirect('/users')
    return render_template('q2.html')

@app.route('/users')
def users():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM USER_ROLE")
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('q2_result.html', userDetails=userDetails)
    cur.close()

if __name__ == "__main__":
    app.run(debug=True)










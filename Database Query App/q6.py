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
        global ID1
        ID1 = userDetails['rid']
        print(ID1)
        return redirect('/q6')
    return render_template('q6.html')


@app.route('/q6')
def users():
    cur = mysql.connection.cursor()
    stmt1 = "SELECT R.RoleName, A.Ap_Operation, R.Description "
    stmt2 = "FROM USER_ROLE as R, Account_Privilege as A "
    stmt3 = "WHERE R.Rid=A.Ap_id AND R.Rid=%s"
    stmt_final = stmt1 + stmt2 + stmt3

    resultValue = cur.execute(stmt_final, ID1)
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('q6_result.html', userDetails=userDetails)
    else:
        return render_template('error.html')
    cur.close()

if __name__ == "__main__":
    app.run(debug=True)
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
        return redirect('/q7')
    return render_template('q7.html')


@app.route('/q7')
def users():
    cur = mysql.connection.cursor()
    stmt1 = "select T.TableName, R.RoleName, RP.Rp_operation, R.Description "
    stmt2 = "from user_role as R, security.table as T, relation_privilege as RP "
    stmt3 = "where R.Rid = T.TableId "
    stmt_and_1 = "and R.Rid = RP.Rp_id "
    stmt_and_2 = "and R.Rid = %s"
    stmt_final = stmt1 + stmt2 + stmt3 + stmt_and_1 + stmt_and_2

    resultValue = cur.execute(stmt_final, ID1)
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('q7_result.html', userDetails=userDetails)
    return render_template('error.html')
    cur.close()

if __name__ == "__main__":
    app.run(debug=True)
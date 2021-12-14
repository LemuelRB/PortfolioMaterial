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
        dataDetails = request.form
        TableName = dataDetails['TableName']
        OwnerName = dataDetails['OwnerName']
        TableId = dataDetails['TableID']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO SECURITY.TABLE(TableId, TableName, OwnerName) VALUES(%s, %s, %s)", (TableId, TableName, OwnerName))
        mysql.connection.commit()
        cur.close()
        return redirect('/users')
    return render_template('q3.html')


@app.route('/users')
def users():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM SECURITY.TABLE")
    if resultValue > 0:
        dataDetails = cur.fetchall()
        return render_template('q3_result.html', dataDetails=dataDetails)
    cur.close()


if __name__ == "__main__":
    app.run(debug=True)
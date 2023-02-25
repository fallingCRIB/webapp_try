from flask import Flask, render_template, request, url_for, redirect, flash
import psycopg2
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.secret_key = 'testKey'
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://postgres:postgres@localhost:5432/app"
db = SQLAlchemy(app)
migrate = Migrate(app, db)
msg = ""


class DataInput(db.Model):
    __tablename__ = "daily_tran_tbl"
    __table_args__ = {"schema": "core"}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    unit = db.Column(db.String())
    salary = db.Column(db.Integer)

    def __init__(self, name, unit, salary):
        self.name = name
        self.unit = unit
        self.salary = salary

    def __repr__(self):
        return f"<Name {self.name}>"


@app.route("/output/")
def output():
    emps = DataInput.query.all()
    return render_template("queryOut.html", outLst=emps)

# DB Connection setup


def get_db_connection():
    conn = psycopg2.connect(
        host="evosfncll235",
        database="NEDTRY",
        port="5431",
        user="postgres",
        password="postgres1",
    )
    return conn


# home landing page
@app.route("/")
def home():
    emps = DataInput.query.all()
    return render_template("index.html", outLst=emps)


@app.route("/select/<lines>")
def selectQuery(lines):
    conn = get_db_connection()
    cur = conn.cursor()
    queryExe = "SELECT * FROM TBAADM.AUDIT_TABLE LIMIT " + lines + ";"
    cur.execute(queryExe)
    books = cur.fetchall()
    cur.close()
    conn.close()
    # return books
    return render_template("queryOut.html", book=books)


@app.route("/input/", methods=["POST", "GET"])
def inputData():

    if request.method == "POST":
        name = request.form["name"]
        unit = request.form["unit"]
        salary = request.form["salary"]
        newEmp = DataInput(name=name, unit=unit, salary=salary)
        db.session.add(newEmp)
        db.session.commit()
        flash("Employee added successfully!!")
        return redirect(url_for("inputData"))
        # return redirect(url_for("selectQuery", lines=name))

    else:
        return render_template("inputForm.html", msgIn=msg)


# App run
if __name__ == "__main__":
    app.run(debug=True)

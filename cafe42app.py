from flask import Flask,render_template,request,redirect,url_for,flash,session
from flask_session import Session
import pandas as pd
from datetime import timedelta
import sqlite3 as sql

app = Flask(__name__)
app.config["SECRET_KEY"] = 'Cafe42SalesBySundeepReddy'
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)

@app.route("/login")
def login():
    return render_template("login.html", title = '- Login')

@app.route("/logout")
def logout():
    session['logged_in'] = False
    flash('Logged out. Please Login', 'info')
    return redirect(url_for("login"))

@app.route("/login", methods = ["POST"])
def post_login():
    username = request.form.get("username")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False
    con = sql.connect("cafe42.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM cafe42users WHERE UNAME = ? AND PASSWORD = ?", (username, password))
    if not cur.fetchall():
        flash('Please check Username or Password and try again.', 'danger')
        return redirect(url_for("login"))
    session['logged_in'] = True
    flash("Welcome", 'success')
    return redirect(url_for("home"))

@app.route("/")
@app.route("/home")
def home():
    if ('logged_in' not in session) or (session['logged_in'] != True):
        flash('Logged out. Please Login', 'info')
        return redirect(url_for("login"))
    con = sql.connect("cafe42.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM cafe42sales ORDER BY DATE DESC")
    data = cur.fetchall()
    return render_template("index.html", title = '- Home', datas = data)

@app.route("/addEntry", methods = ['POST','GET'])
def addEntry():
    if ('logged_in' not in session) or (session['logged_in'] != True):
        flash('Logged out. Please Login', 'info')
        return redirect(url_for("login"))
    if request.method == 'POST':
        name = request.form.get('name')
        item = request.form.get('item').split(" ")[0]
        date = request.form.get('date')
        quantity = request.form.get('quantity')
        total = int(request.form.get('item').split("Rs.")[1])*int(quantity)
        con = sql.connect("cafe42.db")
        cur = con.cursor()
        cur.execute("INSERT INTO cafe42sales (NAME, ITEM, QUANTITY, TOTAL, DATE) VALUES (?,?,?,?,?)", (name, item, quantity, total, date))
        con.commit()
        flash('New Entry Added', 'success')
        return redirect(url_for("home"))
    return render_template("addEntry.html", title = '- Add Entry')

@app.route("/editEntry/<string:uid>", methods = ['POST','GET'])
def editEntry(uid):
    if ('logged_in' not in session) or (session['logged_in'] != True):
        flash('Logged out. Please Login', 'info')
        return redirect(url_for("login"))
    if request.method == 'POST':
        name = request.form.get('name')
        item = request.form.get('item').split(" ")[0]
        date = request.form.get('date')
        quantity = request.form.get('quantity')
        total  =  int(request.form.get('item').split("Rs.")[1])*int(quantity)
        con = sql.connect("cafe42.db")
        cur = con.cursor()
        cur.execute("UPDATE cafe42sales SET NAME = ?, ITEM = ?, QUANTITY = ?, TOTAL = ?, DATE = ? WHERE UID = ?", (name, item, quantity, total, date, uid))
        con.commit()
        flash('Selected Entry Updated', 'success')
        return redirect(url_for("home"))
    con = sql.connect("cafe42.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM cafe42sales WHERE UID = ?",(uid,))
    data = cur.fetchone()
    return render_template("editEntry.html", title = 'Edit Entry', datas = data)
    
@app.route("/deleteEntry/<string:uid>", methods = ['GET'])
def deleteEntry(uid):
    if ('logged_in' not in session) or (session['logged_in'] != True):
        flash('Logged Out. Please Login Again', 'info')
        return redirect(url_for("login"))
    con = sql.connect("cafe42.db")
    cur = con.cursor()
    cur.execute("DELETE FROM cafe42sales WHERE UID = ?", (uid,))
    con.commit()
    flash('Selected Entry Deleted','warning')
    return redirect(url_for("home"))
    
@app.route("/summary", methods = ['POST', 'GET'])
def summary():
    if ('logged_in' not in session) or (session['logged_in'] != True):
        flash('Logged out. Please Login', 'info')
        return redirect(url_for("login"))
    con = sql.connect("cafe42.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM cafe42sales ORDER BY DATE DESC")
    data = cur.fetchall()
    df = pd.DataFrame(data, columns = ['UID', 'NAME', 'ITEM', 'QUANTITY', 'TOTAL', 'DATE', 'ENTRYDATE'])
    name, dates, totals  = '', '', ''
    if request.method == 'POST':
        name = request.form.get('name')
        chartdf = df[df.NAME == name].groupby('DATE').sum(numeric_only=True).reset_index()
        dates = list(chartdf.DATE)
        totals  = list(chartdf.TOTAL)
    return render_template("summary.html", title = '- Summary', name = name, chartData = [dates, totals])

if __name__ == '__main__':
    app.run(debug = True)
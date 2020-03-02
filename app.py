from flask import Flask, render_template, g, request, redirect
import sqlite3

app = Flask(__name__)
DATABASE = 'backpack.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
    return

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/inventory' , methods=["GET", "POST"])
def index(): 
        cursor = get_db().cursor()
        sql = "SELECT * FROM inventory"
        cursor.execute(sql)
        results = cursor.fetchall()
        return render_template('items.html', results=results)
def inventory():
    if request.method == "POST":
        cursor = get_db().cursor()
        new_inventory_name = request.form['inventory_name']
        new_inventory_description = request.form["inventory_description"]
        new_inventory_stat = request.form["inventory_stat"]
        sql = "INSERT INTO inventory(name, description, stat) VALUES (?,?,?)"
        cursor.execute(sql,(new_inventory_name, new_inventory_description, new_inventory_stat))
        get_db().commit()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)

 
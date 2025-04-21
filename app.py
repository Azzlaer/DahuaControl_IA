# app.py - Interfaz web de visualización
from flask import Flask, render_template, g
import sqlite3

app = Flask(__name__)
DATABASE = 'eventos.db'

# Conexión a la base de datos
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

@app.route('/')
def index():
    cursor = get_db().cursor()
    cursor.execute("SELECT patente, archivo, fecha FROM eventos ORDER BY id DESC")
    eventos = cursor.fetchall()
    return render_template('index.html', eventos=eventos)

if __name__ == '__main__':
    app.run(debug=True)

# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'
DATABASE = 'budget.db'
DAYS_IN_MONTH = 30  # Utilisé pour multiplier les dépenses fixes

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    # Table pour les transactions variables (dépenses quotidiennes)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,  -- 'dépense'
            category TEXT NOT NULL,
            description TEXT,
            amount REAL NOT NULL,
            date TEXT NOT NULL
        )
    """)
    # Table pour les revenus mensuels
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS incomes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            date TEXT NOT NULL
        )
    """)
    # Table pour les dépenses fixes quotidiennes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fixed_expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            description TEXT,
            date TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

init_db()

@app.route("/")
def index():
    conn = get_db_connection()
    transactions = conn.execute("SELECT * FROM transactions ORDER BY date DESC").fetchall()
    incomes = conn.execute("SELECT * FROM incomes ORDER BY date DESC").fetchall()
    fixed_expenses = conn.execute("SELECT * FROM fixed_expenses ORDER BY date DESC").fetchall()
    conn.close()

    total_expenses = sum(t['amount'] for t in transactions)
    total_income = sum(i['amount'] for i in incomes)
    total_fixed = sum(f['amount'] for f in fixed_expenses) * DAYS_IN_MONTH

    # Calcul du solde net (revenu - dépenses variables - dépenses fixes)
    solde = total_income - total_expenses - total_fixed

    # Conversion (exemple de taux)
    conversion_rates = {"USD": 600, "EUR": 700}
    solde_usd = solde / conversion_rates["USD"] if solde else 0
    solde_eur = solde / conversion_rates["EUR"] if solde else 0

    # Formatage des montants sans décimales inutiles
    def fmt(n):
        return f"{n:.0f}" if n == round(n) else f"{n:.2f}"

    return render_template("index.html",
                           transactions=transactions,
                           incomes=incomes,
                           fixed_expenses=fixed_expenses,
                           total_income=fmt(total_income),
                           total_expenses=fmt(total_expenses),
                           total_fixed=fmt(total_fixed),
                           solde=fmt(solde),
                           solde_usd=fmt(solde_usd),
                           solde_eur=fmt(solde_eur),
                           conversion_rates=conversion_rates)

@app.route("/add_expense", methods=["GET", "POST"])
def add_expense():
    if request.method == "POST":
        category = request.form["category"]
        description = request.form["description"]
        amount = float(request.form["amount"])
        date = request.form["date"]
        conn = get_db_connection()
        conn.execute("INSERT INTO transactions (type, category, description, amount, date) VALUES (?, ?, ?, ?, ?)",
                     ("dépense", category, description, amount, date))
        conn.commit()
        conn.close()
        flash("Dépense ajoutée avec succès !", "success")
        return redirect(url_for("index"))
    return render_template("add_expense.html")

@app.route("/add_income", methods=["GET", "POST"])
def add_income():
    if request.method == "POST":
        amount = float(request.form["amount"])
        date = request.form["date"]
        conn = get_db_connection()
        conn.execute("INSERT INTO incomes (amount, date) VALUES (?, ?)", (amount, date))
        conn.commit()
        conn.close()
        flash("Revenu mensuel ajouté avec succès !", "success")
        return redirect(url_for("index"))
    return render_template("add_income.html")

@app.route("/add_fixed_expense", methods=["GET", "POST"])
def add_fixed_expense():
    if request.method == "POST":
        amount = float(request.form["amount"])
        description = request.form["description"]
        date = request.form["date"]
        conn = get_db_connection()
        conn.execute("INSERT INTO fixed_expenses (amount, description, date) VALUES (?, ?, ?)",
                     (amount, description, date))
        conn.commit()
        conn.close()
        flash("Dépense fixe ajoutée avec succès !", "success")
        return redirect(url_for("index"))
    return render_template("add_fixed_expense.html")

if __name__ == "__main__":
    print("Lancement du serveur Flask sur http://127.0.0.1:5000")
    app.run(debug=True)


import os
import sqlite3
from flask import Flask, g, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.config["SECRET_KEY"] = "super-secret-key"
DATABASE = "database.db"

def get_db():
    # Uses Flask's g (requires app/app_context)
    db = getattr(g, "_db", None)
    if db is None:
        db = g._db = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_db(exception):
    db = getattr(g, "_db", None)
    if db:
        db.close()

def init_db():
    db = get_db()
    with open("schema.sql", "r", encoding="utf-8") as f:
        db.executescript(f.read())
    with open("sample_data.sql", "r", encoding="utf-8") as f:
        db.executescript(f.read())
    db.commit()

@app.route("/init")
def init():
    init_db()
    flash("Database initialized!")
    return redirect(url_for("home"))

@app.route("/")
def home():
    db = get_db()
    featured = db.execute("""
        SELECT p.ProductID, p.Name, p.Price, p.ImageURL
        FROM Products p
        ORDER BY p.ProductID DESC
        LIMIT 4
    """).fetchall()

    categories = db.execute("SELECT * FROM Categories ORDER BY Name").fetchall()
    return render_template("home.html", featured=featured, categories=categories)

@app.route("/products")
def products():
    db = get_db()
    q = request.args.get("q", "")
    category = request.args.get("category", "")  # CategoryID

    sql = """
        SELECT p.*, c.Name as CatName
        FROM Products p
        JOIN Categories c ON c.CategoryID = p.CategoryID
        WHERE 1=1
    """
    params = []

    if q:
        sql += " AND (p.Name LIKE ? OR p.Description LIKE ?)"
        params += [f"%{q}%", f"%{q}%"]

    if category:
        sql += " AND c.CategoryID = ?"
        params.append(category)

    sql += " ORDER BY p.ProductID DESC"

    items = db.execute(sql, params).fetchall()
    categories = db.execute("SELECT * FROM Categories ORDER BY Name").fetchall()

    return render_template("products.html", items=items, categories=categories, q=q, current_cat=str(category))

@app.route("/products/<int:pid>")
def product_detail(pid):
    db = get_db()
    item = db.execute("""
        SELECT p.*, c.Name as CatName
        FROM Products p
        JOIN Categories c ON c.CategoryID = p.CategoryID
        WHERE ProductID = ?
    """, (pid,)).fetchone()

    if not item:
        flash("Product not found")
        return redirect(url_for("products"))

    return render_template("product_detail.html", item=item)

@app.route("/cart/add/<int:pid>")
def cart_add(pid):
    cart = session.get("cart", {})
    cart[str(pid)] = cart.get(str(pid), 0) + 1
    session["cart"] = cart
    flash("Added to cart")
    return redirect(url_for("cart"))

@app.route("/cart")
def cart():
    db = get_db()
    cart = session.get("cart", {})
    products = []
    total = 0

    for pid, qty in cart.items():
        row = db.execute("SELECT * FROM Products WHERE ProductID=?", (pid,)).fetchone()
        if row:
            amt = row["Price"] * qty
            total += amt
            products.append({
                "id": pid,
                "name": row["Name"],
                "price": row["Price"],
                "image": row["ImageURL"],
                "qty": qty,
                "amount": amt
            })

    return render_template("cart.html", products=products, total=total)

@app.route("/cart/remove/<int:pid>")
def cart_remove(pid):
    cart = session.get("cart", {})
    cart.pop(str(pid), None)
    session["cart"] = cart
    return redirect(url_for("cart"))

if __name__ == "__main__":
    # FIX: use app.app_context() before calling init_db()
    if not os.path.exists(DATABASE):
        with app.app_context():
            init_db()
    app.run(debug=True)

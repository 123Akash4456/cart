from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongodb+srv://neil:12345@cluster0.zdqgpe9.mongodb.net/")
db = client["test"]
items= db
@app.route("/")
def index():
  return render_template("index.html")

@app.route("/add-item", methods=["POST"])
def add_item():
  item = request.form["item"]
  db.items.insert_one({"item": item})
  return "Item added successfully"

@app.route("/show-items")
def show_items():
  items = db.items.find()
  return render_template("show_items.html", items=items)

@app.route("/add-to-cart", methods=["POST"])
def add_to_cart():
  item_id = request.form["item_id"]
  user_id = request.form["user_id"]
  db.carts.insert_one({"item_id": item_id, "user_id": user_id})
  return "Item added to cart successfully"

@app.route("/show-cart")
def show_cart():
  user_id = request.form["user_id"]
  items = db.carts.find({"user_id": user_id})
  return render_template("show_cart.html", items=items)

@app.route("/checkout")
def checkout():
  user_id = request.form["user_id"]
  items = db.carts.find({"user_id": user_id})
  total = 0
  for item in items:
    total += item["item_price"]
  db.orders.insert_one({"user_id": user_id, "items": items, "total": total})
  return "Order placed successfully"

if __name__ == "__main__":
  app.run(debug=True)
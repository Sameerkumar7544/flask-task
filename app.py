from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# MongoDB Atlas connection
client = MongoClient(os.getenv("MONGO_URI"))

db = client["flask_app"]
collection = db["users"]


@app.route("/")
def home():
    return render_template("form.html")


@app.route("/submit", methods=["POST"])
def submit():
    try:
        name = request.form.get("name")
        email = request.form.get("email")

        # Basic validation
        if not name or not email:
            return render_template(
                "form.html",
                error="Name and email are required."
            )

        data = {
            "name": name,
            "email": email
        }

        # Insert into MongoDB Atlas
        collection.insert_one(data)

        # Success
        return redirect(url_for("success"))

    except Exception as e:
        # Error stays on same page
        return render_template(
            "form.html",
            error=str(e)
        )


@app.route("/submittodoitem", methods=["POST"])
def submit_todo_item():
    try:
        item_name = request.form.get("itemName")
        item_description = request.form.get("itemDescription")

        if not item_name or not item_description:
            return "Item Name and Item Description are required.", 400

        todo_data = {
            "itemName": item_name,
            "itemDescription": item_description
        }

        # Store To-Do item in MongoDB
        db["todos"].insert_one(todo_data)

        return "To-Do item saved successfully."

    except Exception as e:
        return str(e), 500


@app.route("/success")
def success():
    return render_template("success.html")


if __name__ == "__main__":
    app.run(debug=True)
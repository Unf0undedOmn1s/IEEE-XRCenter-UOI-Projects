from flask import Flask, render_template, request
import secrets
import string

app = Flask(__name__)

def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for _ in range(length))

@app.route("/", methods=["GET", "POST"])
def index():
    password = ""
    if request.method == "POST":
        length = int(request.form.get("length", 12))
        password = generate_password(length)
    return render_template("index.html", password=password)

if __name__ == "__main__":
    app.run(debug=True)

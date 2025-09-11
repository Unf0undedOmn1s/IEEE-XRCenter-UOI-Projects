from flask import Flask, render_template, request
from generator import generate_password
from safepass import is_password_safe

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    password = ""
    safe = None
    if request.method == "POST":
        length = int(request.form.get("length", 12))
        password = generate_password(length)
        safe = is_password_safe(password, min_length=length if length > 12 else 12)
    return render_template("index.html", password=password, safe=safe)

if __name__ == "__main__":
    app.run(debug=True)

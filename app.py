from flask import Flask, render_template

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URL"] = "sqlite:///database\\baseuno.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.static_folder = "static"

@app.route("/")
def home():
    return render_template("main.html")

if __name__ == "__main__":
    app.run(debug=True, port=4000)
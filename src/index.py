from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/trabajos")
def getTrabajos():
    return render_template("trabajos.html")


if __name__ == "__main__":
    app.run(debug=True)

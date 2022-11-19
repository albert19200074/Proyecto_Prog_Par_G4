from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import threading as th
from classes.CompuTrabajo import CompuTrabajo
from classes.Bumeran import Bumeran
import json

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/trabajos", methods=["POST"])
def searchJob():
    # with open("data/data.json", "w") as file:
    #     json.dump(
    #         [],
    #         file,
    #     )

    # hilo1 = th.Thread(target=Bumeran.main, args=(request.form["nombreTrabajo"],))
    # hilo2 = th.Thread(target=CompuTrabajo.main, args=(request.form["nombreTrabajo"],))

    # hilo1.start()
    # hilo2.start()

    # hilo1.join()
    # hilo2.join()

    with open("data/data.json", "r", encoding="utf8") as file:
        file_data = json.load(file)

    return jsonify(file_data)
    # return render_template("trabajos.html")


@app.route("/trabajos", methods=["GET"])
def getJob():
    return render_template("trabajos.html")


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request
from selenium import webdriver
from bs4 import BeautifulSoup

from selenium.webdriver.firefox.service import Service as FireFoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options as FireFoxOption

import time
import threading as th
import json

app = Flask(__name__)

options = FireFoxOption()
options.headless = True

inicio = True

lock = th.Lock()


def open_json():
    with open("data.json", "r+", encoding="utf8") as file:
        file_data = json.load(file)
        return file_data


def write_json(new_data):
    lock.acquire()
    with open("data.json", "r+", encoding="utf8") as file:
        file_data = json.load(file)
        file_data.append(new_data)
        file.seek(0)
        json.dump(
            file_data,
            file,
            ensure_ascii=False,
            indent=2,
        )
    lock.release()


def delete_json():
    with open("data.json", "w") as file:
        json.dump(
            [],
            file,
            ensure_ascii=False,
            indent=2,
        )


def installerDriverB():
    global _browser_bumeran

    _browser_bumeran = webdriver.Firefox(
        service=FireFoxService(GeckoDriverManager().install()),
        options=options,
    )


def installerDriverC():
    global _browser_compu

    _browser_compu = webdriver.Firefox(
        service=FireFoxService(GeckoDriverManager().install()),
        options=options,
    )


@app.route("/")
def home():
    global inicio
    global hilo_inst_b
    global hilo_inst_c

    if inicio:
        hilo_inst_b = th.Thread(target=installerDriverB)
        hilo_inst_c = th.Thread(target=installerDriverC)

        hilo_inst_b.start()
        hilo_inst_c.start()

        inicio = False

    return render_template("home.html")


@app.route("/trabajos", methods=["POST"])
def searchJob():
    delete_json()

    # Remplazo de tildes y ñ
    trans = str.maketrans("áéíóúüñ", "aeiouun")
    jobName = request.form["nombreTrabajo"].translate(trans).lower().replace(" ", "-")
    placeName = request.form["nombreUbicacion"].lower().replace(" ", "-")

    def Bumeran():

        # URLs
        url = "https://www.bumeran.com.pe"

        if placeName == "todo-el-país":
            key = f"/empleos-busqueda-{jobName}.html"
        elif placeName == "cusco":
            key = f"/en-cuzco/empleos-busqueda-{jobName}.html"
        elif placeName == "callao":
            key = f"/en-gobierno-regional-del-callao/empleos-busqueda-{jobName}.html"
        else:
            key = f"/en-{placeName}/empleos-busqueda-{jobName}.html"

        urlBusqueda = url + key

        hilo_inst_b.join()

        # Ingreso a la pagina
        _browser_bumeran.get(urlBusqueda)

        time.sleep(0.5)

        # Página
        page = BeautifulSoup(_browser_bumeran.page_source, "html.parser")

        # Empleos
        jobs = page.find_all("div", {"class": "sc-cXHFlN"})

        # Guardar Empleos
        for job in jobs:
            link = url + job.find("a").get("href")
            cargo = job.find("h2").text
            empresa = job.find_all("h3")[0].text
            fecha_publicacion = job.find_all("h3")[2].text
            lugar = job.find_all("h3")[3].text

            write_json(
                {
                    "pagina": "Bumeran",
                    "enlace": link,
                    "cargo": cargo,
                    "empresa": empresa,
                    "publicacion": fecha_publicacion,
                    "ubicacion": lugar,
                }
            )

    def CompuTrabajo():

        # URLs
        url = "https://pe.computrabajo.com"

        if placeName == "todo-el-país":
            key = f"/trabajo-de-{jobName}"
        else:
            key = f"/trabajo-de-{jobName}-en-{placeName}"

        urlBusqueda = url + key

        hilo_inst_c.join()

        # Ingreso a la pagina
        _browser_compu.get(urlBusqueda)

        time.sleep(0.5)

        # Página
        page = BeautifulSoup(_browser_compu.page_source, "html.parser")

        # Empleos
        jobs = page.find_all("article", {"class": "box_offer"})

        # Guardar Empleos
        for job in jobs:
            v = True
            link = url + job.find("a", {"class": "js-o-link"}).get("href")
            cargo = job.find("a", {"class": "js-o-link"}).text.strip()
            try:
                empresa = job.find_all("a", {"class": "fc_base"})[1].text.strip()
                if empresa == "Postular":
                    empresa = job.find(
                        "p", {"class": "fs16 fc_base mt5 mb5"}
                    ).text.strip()
                    empresa = empresa[: empresa.find("\n")]
            except:
                empresa = job.find("p", {"class": "fs16 fc_base mt5 mb5"}).text.strip()
                empresa = empresa[: empresa.find("\n")]

                if placeName != "Todo-el-país":
                    lugar = placeName.replace("-", " ")
                    lugar = lugar.capitalize()
                else:
                    lugar = "Sin Información"

                v = False
            if v:
                try:
                    lugar = (
                        job.find("p", {"class": "fs16 fc_base mt5 mb5"})
                        .contents[-1]
                        .text.strip()
                    )
                except:
                    lugar = "Sin Información"
            fecha_publicacion = job.find("p", {"class": "fs13 fc_aux"}).text.strip()

            write_json(
                {
                    "pagina": "CompuTrabajo",
                    "enlace": link,
                    "cargo": cargo,
                    "empresa": empresa,
                    "publicacion": fecha_publicacion,
                    "ubicacion": lugar,
                }
            )

    hilo1 = th.Thread(target=CompuTrabajo, name="Compu")
    hilo2 = th.Thread(target=Bumeran, name="Bumeran")

    hilo1.start()
    hilo2.start()

    hilo1.join()
    hilo2.join()

    lista_empleos = open_json()

    return render_template("trabajos.html", lista_empleos=lista_empleos)


if __name__ == "__main__":
    app.run(debug=True)

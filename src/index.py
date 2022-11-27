from flask import Flask, render_template, request
from selenium import webdriver
from bs4 import BeautifulSoup

from selenium.webdriver.firefox.service import Service as FireFoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options as FireFoxOption

import time
import threading as th

app = Flask(__name__)
# app.config["JSON_AS_ASCII"] = False

options = FireFoxOption()
options.headless = True

inicio = True


def inicializarC():
    global _browser1

    _browser1 = webdriver.Firefox(
        service=FireFoxService(GeckoDriverManager().install()),
        options=options,
    )


def inicializarB():
    global _browser2

    _browser2 = webdriver.Firefox(
        service=FireFoxService(GeckoDriverManager().install()),
        options=options,
    )


@app.route("/")
def home():
    global inicio

    if inicio:
        hilo1 = th.Thread(target=inicializarC)
        hilo2 = th.Thread(target=inicializarB)

        hilo1.start()
        hilo2.start()

        hilo1.join()
        hilo2.join()

        inicio = False
    return render_template("home.html")


@app.route("/trabajos", methods=["POST"])
def searchJob():
    lock = th.Lock()

    # Remplazo de tildes y ñ
    trans = str.maketrans("áéíóúüñ", "aeiouun")
    jobName = request.form["nombreTrabajo"].translate(trans).lower().replace(" ", "-")
    placeName = request.form["nombreUbicacion"].lower().replace(" ", "-")

    lista_empleos = []

    def save_list(data):
        lock.acquire()
        lista_empleos.append(data)
        lock.release()

    def Bumeran():

        # URLs
        url = "https://www.bumeran.com.pe"

        if placeName == "todo-el-país":
            key = f"/empleos-busqueda-{jobName}.html"
        elif placeName == "cusco":
            key = f"/en-cuzco/empleos-busqueda-{jobName}.html"
        else:
            key = f"/en-{placeName}/empleos-busqueda-{jobName}.html"

        urlBusqueda = url + key

        # Ingreso a la pagina
        _browser1.get(urlBusqueda)

        time.sleep(0.5)

        # Página
        page = BeautifulSoup(_browser1.page_source, "html.parser")

        # Empleos
        jobs = page.find_all("div", {"class": "sc-fYAFcb"})

        # Guardar Empleos
        for job in jobs:
            link = url + job.find("a").get("href")
            cargo = job.find("h2").text
            empresa = job.find_all("h3")[0].text
            fecha_publicacion = job.find_all("h3")[2].text
            lugar = job.find_all("h3")[3].text
            modo = job.find_all("h3")[4].text

            save_list(
                {
                    "pagina": "Bumeran",
                    "enlace": link,
                    "cargo": cargo,
                    "empresa": empresa,
                    "publicacion": fecha_publicacion,
                    "ubicacion": lugar,
                }
            )

        # _browser1.close()

    def CompuTrabajo():

        # URLs
        url = "https://pe.computrabajo.com"

        if placeName == "todo-el-país":
            key = f"/trabajo-de-{jobName}"
        else:
            key = f"/trabajo-de-{jobName}-en-{placeName}"

        urlBusqueda = url + key

        # Ingreso a la pagina
        _browser2.get(urlBusqueda)

        time.sleep(0.5)

        # Página
        page = BeautifulSoup(_browser2.page_source, "html.parser")

        # Empleos
        jobs = page.find_all("article", {"class": "box_offer"})

        # Guardar Empleos
        for job in jobs:
            v = True
            link = url + job.find("a", {"class": "js-o-link fc_base"}).get("href")
            cargo = job.find("a", {"class": "js-o-link fc_base"}).text.strip()
            try:
                empresa = job.find(
                    "a", {"class": "fc_base hover it-blank"}
                ).text.strip()
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

            save_list(
                {
                    "pagina": "CompuTrabajo",
                    "enlace": link,
                    "cargo": cargo,
                    "empresa": empresa,
                    "publicacion": fecha_publicacion,
                    "ubicacion": lugar,
                }
            )

        # _browser2.close()

    hilo1 = th.Thread(target=CompuTrabajo, name="Compu")
    hilo2 = th.Thread(target=Bumeran, name="Bumeran")

    hilo1.start()
    hilo2.start()

    hilo1.join()
    hilo2.join()

    return render_template("trabajos.html", lista_empleos=lista_empleos)


if __name__ == "__main__":
    app.run(debug=True)

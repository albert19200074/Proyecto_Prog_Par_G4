from selenium import webdriver
from bs4 import BeautifulSoup

from selenium.webdriver.firefox.service import Service as FireFoxService
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService

from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.firefox.options import Options as FireFoxOption
from selenium.webdriver.chrome.options import Options as ChromeOption
from selenium.webdriver.edge.options import Options as EdgeOption

import time
import json
import configparser
import threading as th


class Main:
    def __init__(self, empleo, ubicacion="Todo el país"):
        self.lock = th.Lock()
        self._config = configparser.ConfigParser()
        self._config.read("config.ini")

        # Remplazo de tildes y ñ
        trans = str.maketrans("áéíóúüñ", "aeiouun")
        self.jobName = empleo.translate(trans).lower().replace(" ", "-")
        self.placeName = ubicacion.lower().replace(" ", "-")

        Main.delete_json()

    def delete_json():
        with open("data.json", "w") as file:
            json.dump(
                [],
                file,
                ensure_ascii=False,
                indent=2,
            )

    def write_json(self, new_data):
        self.lock.acquire()
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
        # print(f"W {th.current_thread().getName()} --> {len(file_data)}")
        self.lock.release()

    def bumeran(self):
        if self._config["BROWSER"]["WEBDRIVER"] == "Firefox":
            options = FireFoxOption()
            options.headless = True

            _browser = webdriver.Firefox(
                service=FireFoxService(GeckoDriverManager().install()),
                options=options,
            )
        elif self._config["BROWSER"]["WEBDRIVER"] == "Chrome":
            options = ChromeOption()
            options.add_argument("start-maximized")

            _browser = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install())
            )
        elif self._config["BROWSER"]["WEBDRIVER"] == "Edge":
            options = EdgeOption()
            options.add_argument("start-maximized")

            _browser = webdriver.Chrome(
                service=EdgeService(EdgeChromiumDriverManager.install()),
                options=options,
            )
        else:
            print(
                "Configurar en el archivo 'config.in' el WEBDRIVER como Firefox, Chrome o Edge"
            )
            exit()

        # URLs
        url = "https://www.bumeran.com.pe"

        if self.placeName == "Todo-el-país":
            key = f"/empleos-busqueda-{self.jobName}.html"
        elif self.placeName == "cusco":
            placeName = "cuzco"
            key = f"/en-{placeName}/empleos-busqueda-{self.jobName}.html"
        else:
            key = f"/en-{self.placeName}/empleos-busqueda-{self.jobName}.html"

        urlBusqueda = url + key

        # Ingreso a la pagina
        _browser.maximize_window()
        _browser.get(urlBusqueda)

        time.sleep(0.5)

        # Página
        page = BeautifulSoup(_browser.page_source, "html.parser")

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

            self.write_json(
                {
                    "pagina": "Bumeran",
                    "enlace": link,
                    "cargo": cargo,
                    "empresa": empresa,
                    "publicacion": fecha_publicacion,
                    "ubicacion": lugar,
                    "modo": modo,
                }
            )

        # Detener

        _browser.close()

    def computrabajo(self):
        if self._config["BROWSER"]["WEBDRIVER"] == "Firefox":
            options = FireFoxOption()
            options.headless = True

            _browser = webdriver.Firefox(
                service=FireFoxService(GeckoDriverManager().install()),
                options=options,
            )
        elif self._config["BROWSER"]["WEBDRIVER"] == "Chrome":
            options = ChromeOption()
            options.add_argument("start-maximized")

            _browser = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install())
            )
        elif self._config["BROWSER"]["WEBDRIVER"] == "Edge":
            options = EdgeOption()
            options.add_argument("start-maximized")

            _browser = webdriver.Chrome(
                service=EdgeService(EdgeChromiumDriverManager.install()),
                options=options,
            )
        else:
            print(
                "Configurar en el archivo 'config.in' el WEBDRIVER como Firefox, Chrome o Edge"
            )
            exit()

        # URLs
        url = "https://pe.computrabajo.com"

        if self.placeName == "Todo-el-país":
            key = f"/trabajo-de-{self.jobName}"
        else:
            key = f"/trabajo-de-{self.jobName}-en-{self.placeName}"

        urlBusqueda = url + key

        # Ingreso a la pagina
        _browser.maximize_window()
        _browser.get(urlBusqueda)

        # Página
        page = BeautifulSoup(_browser.page_source, "html.parser")

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

                if self.placeName != "Todo-el-país":
                    lugar = self.placeName.replace("-", " ")
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

            self.write_json(
                {
                    "pagina": "CompuTrabajo",
                    "enlace": link,
                    "cargo": cargo,
                    "empresa": empresa,
                    "publicacion": fecha_publicacion,
                    "ubicacion": lugar,
                }
            )

        # Detener

        _browser.close()


if __name__ == "__main__":

    buscar = Main("ingeniero de sistemas", "cusco")

    th.Thread(target=buscar.computrabajo, name="C Hilo 1").start()
    # th.Thread(
    #     target=buscar.computrabajo, args=("ingeniero", "lima"), name="C Hilo 2"
    # ).start()
    # th.Thread(
    #     target=buscar.computrabajo, args=("diseño", "cusco"), name="C Hilo 3"
    # ).start()

    th.Thread(target=buscar.bumeran, name="B Hilo 1").start()
    # th.Thread(
    #     target=buscar.bumeran, args=("ingeniero", "arequipa"), name="B Hilo 2"
    # ).start()
    # th.Thread(target=buscar.bumeran, args=("diseño", "cuzco"), name="B Hilo 3").start()

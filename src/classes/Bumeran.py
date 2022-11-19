from selenium import webdriver

from selenium.webdriver.firefox.service import Service as FireFoxService
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService

from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.firefox.options import Options as FireFoxOption
from selenium.webdriver.chrome.options import Options as ChromeOption
from selenium.webdriver.edge.options import Options as EdgeOption

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import json
import configparser
import threading as th

data = "data/data.json"


class Bumeran:
    # function to add to JSON
    def write_json(new_data, filename=data):
        with open(filename, "r+", encoding="utf8") as file:
            # First we load existing data into a dict.
            file_data = json.load(file)
            # Join new_data with file_data inside emp_details
            file_data.append(new_data)
            # Sets file's current position at offset.
            file.seek(0)
            # convert back to json.
            json.dump(
                file_data,
                file,
                ensure_ascii=False,
                indent=2,
            )
        print(f"Bu --> {len(file_data)}")

    @staticmethod
    def main(empleo, ubicacion="Todo el país"):
        nombreEmpleo = empleo
        nombreUbicacion = ubicacion

        _config = configparser.ConfigParser()
        _config.read("../../config.ini")

        if _config["BROWSER"]["WEBDRIVER"] == "Firefox":
            options = FireFoxOption()
            options.headless = True

            _browser = webdriver.Firefox(
                service=FireFoxService(GeckoDriverManager().install()),
                options=options,
            )
        elif _config["BROWSER"]["WEBDRIVER"] == "Chrome":
            options = ChromeOption()
            options.add_argument("start-maximized")

            _browser = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install())
            )
        elif _config["BROWSER"]["WEBDRIVER"] == "Edge":
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
            time.sleep(5)
            exit()

        # Ingreso a la pagina
        _browser.maximize_window()
        _browser.get("https://www.bumeran.com.pe")

        time.sleep(1)

        # Click en Cookies
        WebDriverWait(_browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/w-div/div[3]/a"))
        ).click()

        # Buscar Empleo
        WebDriverWait(_browser, 10).until(
            EC.visibility_of_element_located(
                (
                    By.ID,
                    "react-select-2-input",
                )
            )
        ).send_keys(nombreEmpleo)

        # Búsqueda de Ubicación (Opcional)
        WebDriverWait(_browser, 10).until(
            EC.visibility_of_element_located((By.ID, "react-select-3-input"))
        ).send_keys(nombreUbicacion)

        WebDriverWait(_browser, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "div.select__option--is-focused")
            )
        ).click()

        # Botón entrar
        _browser.find_element(By.ID, "buscarTrabajo").click()

        # Empleos
        cards = WebDriverWait(_browser, 10).until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.sc-jGkVzM"))
        )

        # Dict donde guardaremos los empleos
        datos = {}
        # datos["Bumeran"] = []

        # Guardar Empleos
        i = 0
        for card in cards:
            link = card.find_element(By.TAG_NAME, "a").get_attribute("href")
            nombre = card.find_element(By.TAG_NAME, "h2").text
            empresa = card.find_elements(By.TAG_NAME, "h3")[0].text
            fecha_publicacion = card.find_elements(By.TAG_NAME, "h3")[2].text
            lugar = card.find_elements(By.TAG_NAME, "h3")[3].text
            modo = card.find_elements(By.TAG_NAME, "h3")[4].text

            Bumeran.write_json(
                {
                    "pagina": "Bumeran",
                    "enlace": link,
                    "cargo": nombre,
                    "empresa": empresa,
                    "publicacion": fecha_publicacion,
                    "ubicacion": lugar,
                    "modo": modo,
                }
            )
            if i == 9:
                break
            i += 1

        # Detener

        _browser.close()

        # print(json.dumps(datos, sort_keys=True, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    nombre = "practicante pre profesional"
    ubicacion = "lima"

    th.Thread(
        target=Bumeran.main,
        args=(
            nombre,
            ubicacion,
        ),
    ).start()

    th.Thread(target=Bumeran.main, args=("ingeniero",)).start()

    th.Thread(
        target=Bumeran.main,
        args=(
            "diseño",
            "arequipa",
        ),
    ).start()

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

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import json
import configparser
import threading as th

data = "data/data.json"


class CompuTrabajo:
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
        print(f"Compu --> {len(file_data)}")

    @staticmethod
    def main(empleo):
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

        # Ingreso a la pagina, buscar empleo y búsqueda de ubicación (opcional)
        _browser.maximize_window()

        key = "/trabajo-de-" + empleo.replace(" ", "-")
        url = "https://pe.computrabajo.com"
        urlBusqueda = url + key

        _browser.get(urlBusqueda)

        time.sleep(1)

        page = BeautifulSoup(_browser.page_source, "html.parser")
        work = page.find_all("article", {"class": "box_offer"})

        # Empleos
        # Dict donde guardaremos los empleos
        datos = {}
        datos["CompuTrabajo"] = []

        # Guardar Empleos
        try:
            cook = _browser.find_element(By.XPATH, "/html/body/div[8]/div/a")
            if cook:
                cook.click()
        except:
            try:
                anuncio = _browser.find_element(
                    By.XPATH, "//*[@id='pop-up-webpush-sub']/div[2]/div/button[1]"
                )
                if anuncio:
                    anuncio.click()
            except:
                print()
        finally:
            i = 0
            for elem in work:
                link = elem.find("a", {"class": "js-o-link fc_base"}).get("href")

                trabajo = elem.find("a", {"class": "js-o-link fc_base"}).text.strip()

                try:
                    empresa_ = elem.find(
                        "a", {"class": "fc_base hover it-blank"}
                    ).text.strip()
                except:
                    empresa_ = elem.find(
                        "p", {"class": "fs16 fc_base mt5 mb5"}
                    ).text.strip()
                # puntuacion_ = elem.find("span", {"class": "ml10 mr10"})

                try:
                    ubicacion_ = (
                        elem.find("p", {"class": "fs16 fc_base mt5 mb5"})
                        .contents[-1]
                        .text.strip()
                    )
                except:
                    ubicacion_ = "Sin Información"

                tiempo_ = elem.find("p", {"class": "fs13 fc_aux"}).text.strip()

                CompuTrabajo.write_json(
                    {
                        "pagina": "CompuTrabajo",
                        "enlace": url + link,
                        "cargo": trabajo,
                        "empresa": empresa_,
                        "publicacion": tiempo_,
                        "ubicacion": ubicacion_,
                    }
                )
                if i == 9:
                    break
                i += 1

            # next_btn = _browser.find_element(
            #     By.XPATH, "//*[@id='offersGridOfferContainer']/div[5]/span[2]"
            # )
            # next_btn.click()
            # time.sleep(3)

        # Detener

        _browser.close()

        # print(json.dumps(datos, sort_keys=True, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    empleo = "practicante pre profesional"
    ubicacion = "lima"

    th.Thread(
        target=CompuTrabajo.main,
        args=("ingeniero de sistemas",),
    ).start()
    # th.Thread(target=CompuTrabajo.main, args=("ingeniero")).start()
    # th.Thread(
    #     target=CompuTrabajo.main,
    #     args=("diseño"),
    # ).start()


# for i in range(0, 10):
#     try:
#         cook = _browser.find_element(By.XPATH, "/html/body/div[8]/div/a")
#         if cook:
#             cook.click()
#     except:
#         try:
#             anuncio = _browser.find_element(
#                 By.XPATH, "//*[@id='pop-up-webpush-sub']/div[2]/div/button[1]"
#             )
#             if anuncio:
#                 anuncio.click()
#         except:
#             print()
#     finally:
#         for elem in work:
#             trabajo = elem.find("a", {"class": "js-o-link fc_base"})
#             empresa_ = elem.find("a", {"class": "fc_base hover it-blank"})
#             puntuacion_ = elem.find("span", {"class": "ml10 mr10"})
#             ubicacion_ = elem.find("p", {"class": "fs16 fc_base mt5 mb5"})
#             tiempo_ = elem.find("p", {"class": "fs13 fc_aux"})
#             if trabajo:
#                 nombreTrabajo.append(trabajo.text)
#             else:
#                 nombreTrabajo.append("")
#             if empresa_:
#                 empresa.append(empresa_.text)
#             else:
#                 empresa.append("")
#             if puntuacion_:
#                 puntuacion.append(puntuacion_.text)
#             else:
#                 puntuacion.append("")
#             if ubicacion_ and len(ubicacion_) == 5:
#                 ubi.append(ubicacion_.contents[4])
#             else:
#                 ubi.append("")
#             if tiempo_:
#                 tiempo.append(tiempo_.text)
#             else:
#                 tiempo.append("")

#         next_btn = _browser.find_element(
#             By.XPATH, "//*[@id='offersGridOfferContainer']/div[5]/span[2]"
#         )
#         next_btn.click()
#         time.sleep(3)

# for card in cards:
#     link = card.find_element(By.TAG_NAME, "a").get_attribute("href")
#     nombre = card.find_element(By.TAG_NAME, "h2").text
#     empresa = card.find_elements(By.TAG_NAME, "h3")[0].text
#     fecha_publicacion = card.find_elements(By.TAG_NAME, "h3")[2].text
#     lugar = card.find_elements(By.TAG_NAME, "h3")[3].text
#     modo = card.find_elements(By.TAG_NAME, "h3")[4].text

#     datos["Bumeran"].append(
#         {
#             "Enlace": link,
#             "Cargo": nombre,
#             "Empresa": empresa,
#             "Fecha publicación": fecha_publicacion,
#             "Ubicacion": lugar,
#             "Modo": modo,
#         }
#     )

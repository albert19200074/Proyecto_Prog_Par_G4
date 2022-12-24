# Proyecto_Prog_Par_G4

Proyecto de programacion paralela G4

# TÍTULO: SISTEMA WEB UTILIZANDO WEB SCRAPING Y PROGRAMACIÓN PARALELA PARA MEJORAR LA EFICIENCIA AL EXTRAER DATOS DESDE LA WEB SOBRE OFERTAS LABORALES

---

Sistema web que usará la programación paralela para extraer datos de ofertas laborales de 3 distintas páginas web donde al terminar la ejecución se nos mostrará los resultados encontrados.

---

AUTORES:

1. BENITES NARREA, ELVIS SAUL 19200068
2. CARHUAMACA PUENTE, ALBERT ANTONIO 19200074
3. HERNANDEZ CORDOVA, PIERO JOSUE 19200284
4. HUARCAYA TACAS, EDWARD JOEL 19200113
5. RAMOS VILLANUEVA, SEBASTIAN ELIAS 19200286

---

TEMAS ABORDADOS:

1. SECCIONES CRÍTICA

-  Identificar secciones para que no ocurran deadlock donde los hilos se quiten recursos

3. CONDICIÓN DE CARRERA

-  Para que los hilos no accedan a un mismo recurso en la página web

5. THREADING

-  Para que los hilos no accedan a un mismo recurso en la página web

---

Instalación

```bash

# 1. Instalar virtualenv, en caso no lo tenga
pip install virtualenv

# 2. Crear un entorno virtual con nombre "venv"
python -m venv venv

# 3. Dirigirnos a la carpeta creada Scripts dentro de venv
cd venv/Srcipts

# 4. Instalar las librerías necesarias
pip install -r ../../requirements.txt

# 5. Ejecutar el programa
python ../../src/index.py

# 6. Entrar al siguiente servidor
http://127.0.0.1:5000

```

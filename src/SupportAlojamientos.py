# Importamos las librerías que necesitamos

# Librerías para automatización de navegadores (Selenium)
# -----------------------------------------------------------------------
from selenium import webdriver                   # Control automático del navegador para realizar scraping web
from selenium.webdriver.chrome.service import Service  # Maneja el servicio de ChromeDriver
from selenium.webdriver.common.by import By      # Para seleccionar elementos en la página web (DOM)
from selenium.webdriver.chrome.options import Options  # Configuración de opciones del navegador (headless mode, etc.)
import time                                      # Para gestionar pausas y temporización

# Librerías para extracción de datos y scraping
# -----------------------------------------------------------------------
from bs4 import BeautifulSoup  # Para analizar y extraer datos de HTML y XML (scraping web)

# Librerías para tratamiento y manipulación de datos
# -----------------------------------------------------------------------
import pandas as pd             # Para manipulación de estructuras de datos como DataFrames
import numpy as np              # Para cálculos numéricos y manejo de arrays
import datetime                 # Para manipulación de fechas y tiempos

# Manejo del tiempo y generación de pausas
# -----------------------------------------------------------------------
from time import sleep          # Pausar la ejecución del código durante un tiempo definido

def obtain_html(urls,routes):
    """
    Función para obtener el HTML de varias URLs usando Selenium, hacer clic en el botón de aceptación de cookies
    y guardar el HTML en archivos locales.

    Args:
    urls (list): Lista de URLs de las páginas que se van a scrapeear.
    routes (list): Lista de rutas donde se guardarán los archivos HTML correspondientes.

    Returns:
    None: Esta función no devuelve ningún valor. Los archivos HTML se guardan en las rutas especificadas.
    
    Proceso:
    - Navega a cada URL usando Selenium.
    - Espera a que la página cargue y realiza la acción de aceptar cookies.
    - Extrae el contenido completo de la página después de que el JavaScript haya cargado.
    - Guarda el contenido HTML en un archivo local.
    - Cierra el navegador después de cada iteración.
    """
    for i in range(0,len(urls)):
        # Iniciar el driver
        driver = webdriver.Chrome()
        # Navegar a la página
        driver.get(urls[i])
        sleep(2)
        aceptar_cookies = driver.find_element("css selector", "#react-application > div > div > div:nth-child(1) > div > div.c5vrlhl.atm_mk_1n9t6rb.atm_fq_idpfg4.atm_vy_1osqo2v.atm_wq_z68epy.atm_lk_1ph3nq8.atm_ll_1ph3nq8.sbhok83.atm_p_1wv4lnm.atm_tw_1tftv22.atm_ubcqrc_ccgtyg.atm_p_p3f3nu__1rrf6b5.dir.dir-ltr > section > div > div.mv91188.atm_9s_1txwivl.atm_ar_1bp4okc.atm_gi_1yuitx.atm_h3_8tjzot.atm_h3_1yuitx__oggzyc.atm_ar_vrvcex__oggzyc.dir.dir-ltr > div:nth-child(1) > button")
        aceptar_cookies.click()
        # Esperar a que la página cargue
        time.sleep(2) 
        # Obtener el contenido completo después de cargar el JavaScript
        page_content = driver.page_source
        
        # Usar BeautifulSoup para analizar el HTML
        soup = BeautifulSoup(page_content, "html.parser")

        with open(routes[i], "w", encoding="utf-8") as file:
            file.write(str(soup))
        # Cerrar el navegador
        driver.quit()
    
    return

def make_df(soups):
    """
    Función para extraer datos de varias páginas HTML y convertirlos en un DataFrame de pandas.

    Args:
    soups (list): Lista de objetos BeautifulSoup, cada uno representando una página HTML.

    Returns:
    pd.DataFrame: Un DataFrame que contiene la información extraída, incluyendo título, descripción, precio y fechas de entrada/salida.

    Proceso:
    - Busca en cada página HTML elementos específicos que contengan la información de interés (título, descripción, precio y fechas).
    - Extrae y limpia los datos utilizando BeautifulSoup.
    - Crea un DataFrame temporal para cada página y concatena los resultados en un solo DataFrame final.
    """
    df = pd.DataFrame()
    for soup in soups:
        busqueda_general = soup.find_all("div",{"class":'g1qv1ctd atm_u80d3j_1li1fea atm_c8_o7aogt atm_g3_8jkm7i c1v0rf5q atm_9s_11p5wf0 atm_cx_4wguik atm_dz_7esijk atm_e0_1lo05zz dir dir-ltr'})
        busqueda_fechas = soup.find_all("div",{"class":'f16sug5q atm_c8_1cw7z3g atm_g3_qslrf5 atm_cs_10d11i2 atm_l8_1mni9fk atm_sq_1l2sidv atm_vv_1q9ccgz atm_ks_15vqwwr atm_am_ggq5uc atm_jb_1xtcb10 dir dir-ltr'})
        fechas = [dates.getText() for dates in busqueda_fechas]
        titulos = [nombre.contents[0].getText() for nombre in busqueda_general]
        descripcion = [descripcion.contents[1].getText() for descripcion in busqueda_general]
        precio = [precio.contents[4].getText().split()[7] for precio in busqueda_general]
        print(fechas[1].split(" – ")[0])
        print(fechas[1].split(" – ")[1])

        df_temp = pd.DataFrame({
            "Título":titulos,
            "Descripción":descripcion,
            "Precio (€)":precio,
            "Fecha entrada": fechas[1].split(" – ")[0],
            "Fecha salida": fechas[1].split(" – ")[1]
        })
        df = pd.concat([df,df_temp],ignore_index=True)
    return df
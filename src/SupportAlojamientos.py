# Importamos las librerías que necesitamos
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
# Librerías de extracción de datos
# -----------------------------------------------------------------------
from bs4 import BeautifulSoup
import requests
import tqdm
# Tratamiento de datos
# -----------------------------------------------------------------------
import pandas as pd
import numpy as np
import datetime

# Requests
import requests

from time import sleep
import random

def obtain_html(urls,routes):
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
    df = pd.DataFrame()
    for soup in soups:
        busqueda_general = soup.find_all("div",{"class":'g1qv1ctd atm_u80d3j_1li1fea atm_c8_o7aogt atm_g3_8jkm7i c1v0rf5q atm_9s_11p5wf0 atm_cx_4wguik atm_dz_7esijk atm_e0_1lo05zz dir dir-ltr'})
        busqueda_fechas = soup.find_all("div",{"class":'f16sug5q atm_c8_1cw7z3g atm_g3_qslrf5 atm_cs_10d11i2 atm_l8_1mni9fk atm_sq_1l2sidv atm_vv_1q9ccgz atm_ks_15vqwwr atm_am_ggq5uc atm_jb_1xtcb10 dir dir-ltr'})
        fechas = [dates.getText() for dates in busqueda_fechas]
        titulos = [nombre.contents[0].getText() for nombre in busqueda_general]
        descripcion = [descripcion.contents[1].getText() for descripcion in busqueda_general]
        precio = [precio.contents[4].getText().split()[7] for precio in busqueda_general]
        
        df_temp = pd.DataFrame({
            "Título":titulos,
            "Descripción":descripcion,
            "Precio (€)":precio,
            "Fecha entrada": fechas[1].split(" – ")[0],
            "Fecha salida": fechas[1].split(" – ")[1]
        })
        df = pd.concat([df,df_temp],ignore_index=True)
    return df
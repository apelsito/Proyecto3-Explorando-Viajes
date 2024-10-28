# 🏖️ Proyecto3 - Explorando Viajes 🌍

Este proyecto tiene como objetivo planificar un viaje de fin de semana para un grupo de 4 amigos interesados en hacer turismo en dos destinos posibles: Oslo y Mónaco. El grupo está disponible para viajar durante la última semana de octubre o cualquier fin de semana de noviembre, y ha solicitado una lista de 60 actividades turísticas variadas para disfrutar durante su estancia.

## Descripción del Proyecto 🛫

El proyecto se centra en la recolección y análisis de datos sobre vuelos, alojamientos y actividades turísticas para ambos destinos. Se ha utilizado una combinación de APIs y técnicas de web scraping para obtener información actualizada y detallada sobre:

- Vuelos: Precios, horarios y duración de vuelos de ida y vuelta.
- Alojamientos: Precios y disponibilidad de alojamientos en Mónaco y Oslo (Airbnb).
- Actividades: Se ha recopilado una lista de 60 actividades variadas en cada ciudad para ofrecer una experiencia turística completa.

## Estructura del Proyecto 🗂️

```bash
Proyecto3-Explorando-Viajes/
├── datos/               # Datos crudos y procesados
│   ├── vuelos/          # Información sobre vuelos a Mónaco y Oslo
│   ├── alojamientos/    # Datos de alojamientos Airbnb en ambos destinos
│   ├── actividades/     # Listas de actividades turísticas en Oslo y Mónaco
│   ├── html_backups/    # Html Descargados para hacer beautiful Soup
│   ├── json_backups/    # Jsons descargados para no saturar la API
│   ├── anaconda_prereq/ # Pequeña documentación sobre la creación de Anaconda
├── jupyter_notebooks/   # Notebooks Jupyter con el análisis y las visualizaciones
├── src/  
│    ├── png/            # Fotos de las gráficas
└── README.md            # Descripción del proyecto
```
## Instalación y Requisitos 🛠️
### Requisitos
Para ejecutar este proyecto, asegúrate de tener instalado lo siguiente:

- Python 3.x 🐍
- Jupyter Notebook 📓
- Bibliotecas de Python:
    - [pandas](https://pandas.pydata.org/docs/) para manipulación de datos 🧹
    - [numpy](https://numpy.org/doc/2.1/) para cálculos numéricos 🔢
    - [selenium]()
    - [matplotlib](https://matplotlib.org/stable/index.html)
    - [seaborn](https://seaborn.pydata.org/) para visualización de datos 📊
    - [requests](https://requests.readthedocs.io/en/latest/)
    - [beautifulsoup4](https://beautiful-soup-4.readthedocs.io/en/latest/) para scraping de sitios web 🌐
- API de [Air Scraper](https://rapidapi.com/apiheya/api/sky-scrapper)

### Instalación 🛠️

1. Clona este repositorio y navega al directorio del proyecto:
```bash
git clone https://github.com/apelsito/Proyecto3-Explorando-Viajes.git
cd Proyecto3-Explorando-Viajes
```
# Análisis de las Gráficas obtenidas 📊
Para comprender mejor las opciones de viaje a Oslo y Mónaco, se han elaborado una serie de gráficas que ofrecen una visión detallada de los datos de precios y disponibilidad de alojamientos, así como de los vuelos y valoraciones de las actividades.

Estas visualizaciones ayudan a responder preguntas clave sobre la accesibilidad económica y la conveniencia de cada destino para el grupo de amigos, tomando en cuenta fechas específicas de viaje y rangos de precios.

## Distribución de Calificaciones de Actividades en Mónaco y Oslo

![Distribución de Calificaciones de Actividades en Mónaco y Oslo](src/png/01_grafico_distribucion_calificaciones_por_ciudad.png)

En la gráfica de distribución de calificaciones de actividades en Mónaco y Oslo, observamos una tendencia clara hacia valoraciones altas en ambos destinos.
1. Concentración de Calificaciones:

- **La mayoría de las actividades** en ambas ciudades tienen calificaciones altas, situándose entre 4.0 y 4.5. Esto indica una oferta turística de calidad similar en ambos lugares, con actividades generalmente bien valoradas.
- **La densidad más alta** en cada destino está alrededor de la calificación de 4.5, lo que sugiere que los visitantes de ambos destinos suelen encontrar experiencias satisfactorias.
2. Comparación entre Mónaco y Oslo:

- Aunque ambas ciudades tienen una distribución de calificaciones similar, Mónaco muestra una leve mayor concentración en calificaciones justo por encima de 4.0, mientras que Oslo parece estar ligeramente más concentrado en 4.5.
- Esto puede indicar que las actividade de Oslo están ligeramente mejor valoradas en términos de experiencia general.
3. Rangos de Calificación Menores:

- Notamos muy pocas o ninguna actividad en rangos de calificación inferiores a 4.0, lo que sugiere que, en general, las opciones de actividades en ambas ciudades mantienen un estándar de calidad alto.
- Es poco común encontrar actividades turísticas en estos destinos con calificaciones bajas, lo cual es positivo para quienes buscan experiencias confiables y bien valoradas.

## Top 10 Actividades en Mónaco y Oslo

![Top 10 Mónaco](src/png/02_top_mejores_actividades_monaco.png)![Top 10 Oslo](src/png/03_top_mejores_actividades_oslo.png)



## Conclusiones ✈️

Este análisis ha permitido:

1. Ofrecer dos opciones de destinos turísticos (Oslo y Mónaco) con datos completos sobre vuelos, alojamientos y actividades.
2. Visualizar y comparar los precios medios de alojamientos para diferentes fines de semana.
3. Proporcionar al grupo de amigos una experiencia de viaje personalizada con 60 actividades seleccionadas según sus intereses.

# Contribuciones 🤝

Las contribuciones a este proyecto son muy bienvenidas. Si tienes alguna sugerencia, mejora o corrección, no dudes en ponerte en contacto o enviar tus ideas.

Cualquier tipo de contribución, ya sea en código, documentación o feedback, será valorada. ¡Gracias por tu ayuda y colaboración!

# Autores y Agradecimientos ✍️

## Autor ✒️
**Gonzalo Ruipérez Ojea** - [@apelsito](https://github.com/apelsito) en github

## Agradecimientos
Quiero expresar mi agradecimiento a **Hackio** y su equipo por brindarme la capacidad y las herramientas necesarias para realizar este proyecto con solo una semana de formación. Su apoyo ha sido clave para lograr este trabajo.
# chessrec
An Embedding-Based Recommender System for Chess Opening Suggestions

## Dataset

Debido a que los datos de entrenamiento son muy grandes, no se incluyen en este repositorio. Sin embargo, se pueden descargar desde el siguiente enlace: [ChessRec Data Drive](https://drive.google.com/drive/folders/1t5eMurIJmxTnGY7LdT93jp3xK2WzR3i0?usp=drive_link). Al descargar esta carpeta, se deben ubicar las subcarpetas en el directorio raíz del proyecto. Esta carpeta contiene los datos que se utilizaron a lo largo del desarrollo (encontrados en la carpeta `data`). Además, se incluyen dos de los motores (Dragon y Komodo) utilizados para la evaluación. Notar que Stockfish debe ser instalado por separado, para esto, se deben seguir las indicaciones descritas en la página de [Stockfish](https://stockfishchess.org/download/).

## Código

Para correr los distintos archivos que se presentan, se recomienda crear un ambiente virtual en Python e instalar las librerías que se encuentran en `requirements.txt`.

### data_generation.ipynb

Este notebook se encarga de generar los datos de entrenamiento. Para esto, se leen las partidas utilizando la librería `python-chess`, se extraen las jugadas y se guardan en un archivo `.csv`. Se utilizan las partidas de la base de datos de Lichess del mes de julio de 2014, pero esto puede ser reemplazado por cualquier archivo que se estime conveniente.

### chessrec.ipynb

Este notebook contiene el código principal del proyecto. Se encarga de cargar los datos de entrenamiento, entrenar el modelo y evaluarlo. Además, se incluyen funciones para realizar recomendaciones de aperturas. El proceso correspondiente a la generación de embeddings toma bastante tiempo, por lo que se recomienda usar los archivos `.csv` cargados en la carpeta de datos. En las distintas secciones, se encuentran los procedimientos hechos para obtener el modelo final. La evaluación del modelo es también un punto que toma tiempo considerable, pero es posible correrlo para replicar los resultados mencionados en el paper.

### evaluation.py

Este archivo se encarga de definir las métricas que se utilizan para evaluar las recomendaciones del modelo. Notar que estas funciones contienen métricas para aperturas recomendadas para cuando el jugador juega con negras, que finalmente no fue tomado en cuenta para la versión final del modelo.

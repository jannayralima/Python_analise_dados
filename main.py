#      _                           _     _                 
#     | | __ _ _ __  _ __   __ _  | |   (_)_ __ ___   __ _ 
#  _  | |/ _` | '_ \| '_ \ / _` | | |   | | '_ ` _ \ / _` |
# | |_| | (_| | | | | | | | (_| | | |___| | | | | | | (_| |
#  \___/ \__,_|_| |_|_| |_|\__,_| |_____|_|_| |_| |_|\__,_|

#autor: Janna Lima
#data: 20/09/2025
# Version: 1.0.0

from flask import Flask, request, jsonify, render_template_string
import pandas as pd
import sqlite3
import os
import plotly.graph_objs as go
from dash import Dash, html, dcc
import numpy as  np
import config #Nosso arquivo config.py
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)
pasta = config.FOLDER
caminhoBd = config.DB_PATH
rotas = config.ROTAS
vazio = 0

def init_db():
    with sqlite3.connect (f'{pasta}{caminhoBd}') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS inadimplencia(
                mes TEXT PRIMARY KEY,
                inadimplencia REAL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS SELIC(
                mes TEXT PRIMARY KEY,
                Selic_diaria REAL
            )
        ''')
        conn.commit

@app.route(rotas[0])
def index(): 
    return render_template_string(f'''
        <h1> upload de dados economicos </h1>
        <form action="{rotas[1]}"method="POST" enctype="multipart/form-data">
                                  
            <label for="campo_inadimplencia"> Arquivo de Inadimplencia (CSV): </label>
            <input name="campo_inadimplencia" type="file" required> <br>
                                  
            <label for="campo_selic"> Arquivo de Taxa Selic (CSV): </label>
            <input name="campo_selic" type="file" required><br>

            <input type="submit" value="Fazer upload">  <br>               
            </form>
            <br><br>
            <a href="{rotas[2]}">Consultar dados armazanados </a> <br> 
            <a href="{rotas[3]}"> Visualizar Graficos </a> <br> 
            <a href="{rotas[4]}"> Editar Inadimplencia </a> <br> 
            <a href="{rotas[5]}"> Analisar Correlação </a> <br> 

    ''')

if __name__ == "__main__":
    init_db()
    app.run(
        debug=config.FLASK_DEBUG,
        host = config.FLASK_HOST,
        port = config.FLASK_PORT
    )
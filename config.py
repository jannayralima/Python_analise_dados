#      _                           _     _                 
#     | | __ _ _ __  _ __   __ _  | |   (_)_ __ ___   __ _ 
#  _  | |/ _` | '_ \| '_ \ / _` | | |   | | '_ ` _ \ / _` |
# | |_| | (_| | | | | | | | (_| | | |___| | | | | | | (_| |
#  \___/ \__,_|_| |_|_| |_|\__,_| |_____|_|_| |_| |_|\__,_|

#autor: Janna Lima
#data: 20/09/2025
# Version: 1.0.0

# configurações comuns do sistema

FOLDER = 'C:/Users/sabado/Desktop/Python AD Janna Lima/AIS/'
DB_PATH = 'BANCODEDADOSais.DB'
FLASK_DEBUG =  True
FLASK_HOST = '127.0.0.1'
FLASK_PORT = 5000

## Rotas comuns do sistema
ROTAS = [
    '/',                            #rota 00
    '/upload',                      #rota 01
    '/consultar',                   #rota 02
    '/graficos',                    #rota 03
    '/editar_inadimplencia',        #rota 04
    '/corelação'                    #rota 05
    ]
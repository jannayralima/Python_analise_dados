from flask import Flask, request, render_template_string
import pandas as pd
import sqlite3 
import plotly.express as px
import plotly.io as pio
import random
import os

pio.renderers.default = 'browser'


caminho = "C:/Users/sabado/Desktop/Python AD Janna Lima/"
tabela =  ["drinks.csv", "avengers.csv"]

codHtml = '''
    <h1>  Dashboards - Consumo de Alcool  <h/1>
    <h2> Parte 01 </h2>
        <ul>
                <li><a href="/grafico1"> Top 10 países em consumo de alcool </a></li>
                <li><a href="/grafico2"> Media de consumo por tipo </a></li>
                <li><a href="/grafico3"> Consumo total por região </a></li>
                <li><a href="/grafico4"> Comparativo entre tipos de bebidas </a></li>
                <li><a href="/#"> Insights por país </a></li>
         </ul>
    <h2>  Parte 02 </h2>
        <ul>
                <li><a href="/comparar"> Comparar </a></li>
                <li><a href="/upload"> upload CVS </a></li>
                <li><a href="/apagar"> Apagar tela </a></li>
                <li><a href="/ver"> Ver tabela </a></li>
                <li><a href="/vaa"> V.A.A. (Vingadores Alcolicos Anonimos </a></li>
        </ul>
'''


def carregarCsv():
    #carregar o arquivo drinks 
    #dfDrinks = pd.read_csv(r"C:\Users\sabado\Desktop\Python AD Janna Lima\drinks.csv")
        
    try:
        dfDrinks = pd.read_csv(os.path.join(caminho, tabela[0]))
        dfAAvengers = pd.read_csv(os.path.join(caminho, tabela[1]), encoding = 'latin1')
        return dfDrinks, dfAAvengers
    except Exception as erro:
        print(f'Erro ao carregar as arquivos CSV: {erro}')
        return None, None
    
def criarBancoDados():
    conn = sqlite3.connect(f"{caminho}banco01.bd")
    #carregar dados usando nossa função criada anteriormente
    dfDrinks, dfAvengers = carregarCsv()
    if dfDrinks is None or dfAvengers is None:
        print("falha ao carregar os dados")
        return
    
    #inserir as tabelas no bando de dados
    dfDrinks.to_sql("bebidas", conn, if_exists="replace", index=False)
    dfAvengers.to_sql("vingadores", conn, if_exists="replace", index=False)
    conn.commit()
    conn.close

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string(codHtml)

@app.route('/grafico1')
def grafico1():
    with sqlite3.connect(f'{caminho}banco01.bd') as conn:
        df = pd.read_sql_query('''
            SELECT country, total_litres_of_pure_alcohol
            FROM BEBIDAS
            ORDER BY total_litres_of_pure_alcohol DESC
            LIMIT 10                                       
             ''', conn)
    figuraGrafico01 = px.bar(
        df,
        x = 'country',
        y = 'total_litres_of_pure_alcohol',
        title = 'Top 10 países em consumo de alcool'
    )
    return figuraGrafico01.to_html()

@app.route('/grafico2')
def grafico2():
    with sqlite3.connect(f'{caminho}banco01.bd') as conn:
        df = pd.read_sql_query('''
            SELECT AVG(beer_servings) AS cervejas,
                   AVG(spirit_servings) AS destilados,
                   AVG(wine_servings) AS vinhos
            FROM bebidas                                     
             ''', conn)
        
    df_melted = df.melt(var_name='Bebidas', value_name='Média de Porções')

    figuraGrafico02 = px.bar(
        df_melted,
        x = 'Bebidas',
        y = 'Média de Porções',
        title = 'Média Consumo golbal por tipo'
    )
    return figuraGrafico02.to_html()




@app.route("/grafico3")
def grafico3():
    regioes = {
        "Europa": ['France', 'Germany', 'Spain', 'Italy', 'Portugal'],
        "Asia": ['China','Japan', 'India', 'Thailand'],
        "Africa": ['Angola', 'Nigeria', 'Egypt', 'Algeria'],
        "Americas": ['USA', 'Canada', 'Brazil', 'Argentina', 'Mexico'] 
    }
    dados = []
    with sqlite3.connect(f'{caminho}banco01.bd') as conn:
        # itera sobre o dicionario, de regios onde cada chave (regiao tem uma lista de paises ) 
        for regiao, paises in regioes.items():
            placeholders = ",".join([f"'{pais}'" for pais in paises])
            query = f"""
                SELECT SUM(total_litres_of_pure_alcohol) AS total
                FROM bebidas
                WHERE country IN ({placeholders})
            """

            total = pd.read_sql_query(query, conn).iloc[0,0]
            dados.append({
                "Região": regiao,
                "Consumo Total": total
            })

    dfRegioes = pd.DataFrame(dados)
    figuraGrafico3 = px.pie(
        dfRegioes,
        names= "Região",
        values="Consumo Total",
        title="Consumo total por Região"
    )
    return figuraGrafico3.to_html()

@app.route('/comparar', methods=['POST', 'GET'])
def comparar():
    opcoes = [
        'beer servings',
        'spirit_servings',
        'wine_servings'
    ]

    if request.method == "POST":
        eixoX = request.form.get('eixo_x')
        eixoY = request.form.get('eixo_y')
        if eixoX == eixoY:
            return "<marquee> Você fez besteira... escolha opções diferentes </marquee>"
        
        conn = sqlite3.connect(f'{caminho}banco01.bd')
        df = pd.read_sql_query("SELECT country, {}, {} FROM bebidas".format(eixoX, eixoY),conn)
        conn.close()
        figuraComparar = px.scatter(
            df,
            x = eixoX,
            y = eixoY,
            title=f'Comparação entre {eixoX} VS {eixoY}'
        )
        figuraComparar.update_traces(
            textposition = "top center"
        )

        return figuraComparar.to_html()

    return render_template_string('''                    
                                   
        <style>
        /* Estilo global para reset e fonte limpa */
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(to right, #f0f2f5, #d9e2ec);
    padding: 40px;
    display: flex;
    justify-content: center;
}

/* Estilo do h2 */
h2 {
    text-align: center;
    font-size: 24px;
    color: #333;
    margin-bottom: 30px;
}

/* Estilo do formulário */
form {
    background-color: white;
    padding: 30px 40px;
    border-radius: 12px;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
    width: 100%;
    max-width: 400px;
}

/* Estilo das labels */
label {
    display: block;
    font-weight: bold;
    color: #444;
    margin: 20px 0 8px;
}

/* Estilo dos selects */
select {
    width: 100%;
    padding: 10px;
    border-radius: 6px;
    border: 1px solid #ccc;
    background-color: #fefefe;
    font-size: 15px;
    transition: border-color 0.3s;
}

select:focus {
    border-color: #4a90e2;
    outline: none;
}

/* Estilo do botão de submit */
input[type="submit"] {
    margin-top: 30px;
    background-color: #4a90e2;
    color: white;
    border: none;
    padding: 12px;
    width: 100%;
    font-size: 16px;
    border-radius: 6px;
    cursor: pointer;
    transition: background-color 0.3s;
}

input[type="submit"]:hover {
    background-color: #357ab7;
}

        </style>
        <h2> Comparar Campos </h2>
        <form method="POST">
            <label for="eixo_x"> Eixo X: </label>
            <select name="eixo_x">
                {% for opcao in opcoes %}                
                    <option value="{{opcao}}"> {{opcao}} </option>           
                {% endfor %}   
            </select>
            <br></br>
                                  
            <label for="eixo_y"> Eixo Y </label>
            <select name="eixo_y">
                {% for opcao in opcoes %}
                    <option value="{{opcao}}"> {{opcao}} </option>
                {% endfor %}                 
            </select>
            <br></br>
                                  
            <input type="submit" value= "--Comparar--">
        </form>
     ''', opcoes = opcoes) 







if __name__ == '__main__':
    criarBancoDados()
    app.run(debug=True)
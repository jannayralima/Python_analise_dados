import pandas as pd 
# lets start*,
# carregar dados da planilha
caminho = 'C:/Users/sabado/Desktop/Python AD Janna Lima/01_base_vendas.xlsx'

df1 = pd.read_excel (caminho, sheet_name='Relatório de Vendas')
df2 = pd.read_excel (caminho, sheet_name='Relatório de Vendas1')

#exibir as primeiras linhas das tabelas
print('---------primeiro relatório----------')
print(df1.head())

print('---------segundo relatório-----------')
print(df2.head())

#verificar se existem duplicatas
print('Duplicatas no relatório 01')
print(df1.duplicated().sum())

print('Duplicatas no relatório 02')
print(df2.duplicated().sum())

#vamos consolidar as duas tabelas
print('Dados Consolidados')
dfConsolidado = pd.concat([df1,df2], ignore_index=True)

print(dfConsolidado.head())

#exibir o numero de clientes por cidades
clientesPorCidade = dfConsolidado.groupby('Cidade')['Cliente'].nunique().sort_values(ascending=False)

print ('Clientes por Cidade')
print(clientesPorCidade)

#numero de vendas por plano
vendasPorPlano = dfConsolidado['Plano Vendido'].value_counts()
print ('Números de vendas por plano')
print(vendasPorPlano)

#exibir as 3 cidades com mais clientes
top3Cidades = clientesPorCidade.head(3)
print ('Top 3 Cidades')
print(top3Cidades)

#adicionar nova coluna de status (exemplo ficticio de analises)
#vamos classificar os planos como 'premium' se for enterpise e os demais planos serao 'padrao'

dfConsolidado['Status'] = dfConsolidado['Plano Vendido'].apply(lambda x: 'Premium' if x == 'Enterprise' else 'Padrão')

#exibir a distribuição dos status
statusDist = dfConsolidado ['Status'].value_counts()
print ('Distribuição dos Status:')
print(statusDist)

#Salvar a tabela em arquivo novo 
#primeiro em excel 
dfConsolidado.to_excel('Dados consolidados.xlsx', index=False)
print ('Dados salvos na planilha do excel')

#depois em CSV
dfConsolidado.to_csv('Dados consolidados.csv', index=False)
print ('Dados salvos na planilha em CVS')

#mensagem final

print('---------- PROGRAMA FINALIZADO--------')
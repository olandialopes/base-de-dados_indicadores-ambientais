import pandas as pd

data = pd.read_csv('2-poluentes atmosfericos_dados_ibama.csv', delimiter=';')

# Colunas a serem excluidas
variaveis_excluidas = [
    'Código da Categoria', 'Código do Detalhe', 'Detalhe',
    'Metodologia utilizada', 'Situação Cadastral'
]
# Excluir as variáveis excluidas, cujos nomes estão acima
data = data.drop(columns=variaveis_excluidas, axis=1)

# Excluir linhas com pelo menos uma célula vazia em qualquer coluna
data = data.dropna(how='any')

# Excluir linhas com valores zero em qualquer coluna
data = data[~(data == '0').any(axis=1)]

# Crie uma amostra aleatória de 50% dos dados originais para testar
# data = data.sample(frac=0.5)

# Ordena os CNPJs em ordem alfanumérica
data = data.sort_values(by='CNPJ')

# Obter uma lista de CNPJs únicos
cnpjs_unicos = data['CNPJ'].unique()

# Criar uma lista de dicionários para armazenar os CNPJs únicos e os anos correspondentes
cnpj_anos_list = []

# Iterar pelos CNPJs únicos e encontrar os anos correspondentes
for cnpj in cnpjs_unicos:
    anos = data[data['CNPJ'] == cnpj]['Ano'].unique()
    cnpj_anos_list.append({'CNPJ': cnpj, 'Anos': ', '.join(map(str, anos))})

# Criar um DataFrame a partir da lista de dicionários
cnpj_anos_df = pd.DataFrame(cnpj_anos_list)

# Salvar o resultado em um arquivo CSV
cnpj_anos_df.to_csv('2-emissoes atm_cnp_ano.csv', index=False)

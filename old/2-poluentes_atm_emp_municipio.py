import pandas as pd

data = pd.read_csv('2-poluentes atmosfericos_dados_ibama.csv', delimiter=';')

# Colunas a serem excluidas
variaveis_excluidas = [
    'Código da Categoria', 'Código do Detalhe', 'Detalhe',
    'Metodologia utilizada', 'Situação Cadastral'
]
#Excluir as variáveis excluidas, cujos nomes estão acima
data = data.drop(columns=variaveis_excluidas, axis=1)


# Contar valores únicos de CNPJ em cada município
contagem_empresas_por_municipio = data.groupby('Município')['CNPJ'].nunique()

# Contar quantas vezes cada município aparece
contagem_municipios = data['Município'].value_counts().reset_index()
contagem_municipios.columns = ['Município', 'Quantidade de Empresas']
# Salvar a contagem em um arquivo CSV
contagem_municipios.to_csv('2-contagem_empresas_por_municipio.csv', index=False)

# Excluir linhas com pelo menos uma célula vazia em qualquer coluna
data = data.dropna(how='any')

# Contar valores únicos de CNPJ em cada município
contagem_empresas_por_municipio = data.groupby('Município')['CNPJ'].nunique()
# Contar quantas vezes cada município aparece
contagem_municipios = data['Município'].value_counts().reset_index()
contagem_municipios.columns = ['Município', 'Quantidade de Empresas']
# Salvar a contagem em um arquivo CSV
contagem_municipios.to_csv('2-contagem_empresas_por_municipio2.csv', index=False)

# Excluir linhas com valores zero em qualquer coluna
data = data[~(data == '0').any(axis=1)]

# Contar valores únicos de CNPJ em cada município
contagem_empresas_por_municipio = data.groupby('Município')['CNPJ'].nunique()
# Contar quantas vezes cada município aparece
contagem_municipios = data['Município'].value_counts().reset_index()
contagem_municipios.columns = ['Município', 'Quantidade de Empresas']
# Salvar a contagem em um arquivo CSV
contagem_municipios.to_csv('2-contagem_empresas_por_municipio2.csv', index=False)

# Salvar as alterações de volta no arquivo CSV
data.to_csv('2-result_poluentes_atm.csv', index=False)

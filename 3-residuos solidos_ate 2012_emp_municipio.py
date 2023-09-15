import pandas as pd

data = pd.read_csv('3-relatorio residuos solidos_ibama_ate 2012.csv', delimiter=';')

# Colunas a serem excluidas
variaveis_excluidas = [
'Código da Categoria', 'Categoria de Atividade', 'Código do Detalhe','Detalhe','Cod. Resíduo','Tipo de Resíduo',
    'Tipo de monit. realizado','Tipo de Finalidade', 'Finalidade da Transferência','CNPJ da emp. de Armazen/Destin',
    'Raz. soc. emp. Armazen/Destin','Latitude', 'Longitude','Situação Cadastral',
    'Identif. do Resíduo NBR 10.004', 'Efic. do sist. de tratamento'

    ]
#Excluir as variáveis excluidas, cujos nomes estão acima
data = data.drop(columns=variaveis_excluidas, axis=1)

# Contar valores únicos de CNPJ em cada município
contagem_empresas_por_municipio = data.groupby('Município')['CNPJ do gerador'].nunique()

# Contar quantas vezes cada município aparece
contagem_municipios = data['Município'].value_counts().reset_index()
contagem_municipios.columns = ['Município', 'Quantidade de Empresas']
# Salvar a contagem em um arquivo CSV
contagem_municipios.to_csv('3-contagem_empresas_por_municipio.csv', index=False)

# Excluir linhas com pelo menos uma célula vazia em qualquer coluna
data = data.dropna(how='any')

# Contar valores únicos de CNPJ em cada município
contagem_empresas_por_municipio = data.groupby('Município')['CNPJ do gerador'].nunique()
# Contar quantas vezes cada município aparece
contagem_municipios = data['Município'].value_counts().reset_index()
contagem_municipios.columns = ['Município', 'Quantidade de Empresas']
# Salvar a contagem em um arquivo CSV
contagem_municipios.to_csv('3-contagem_empresas_por_municipio2.csv', index=False)

# Excluir linhas com valores zero em qualquer coluna
data = data[~(data == '0').any(axis=1)]

# Contar valores únicos de CNPJ em cada município
contagem_empresas_por_municipio = data.groupby('Município')['CNPJ do gerador'].nunique()
# Contar quantas vezes cada município aparece
contagem_municipios = data['Município'].value_counts().reset_index()
contagem_municipios.columns = ['Município', 'Quantidade de Empresas']
# Salvar a contagem em um arquivo CSV
contagem_municipios.to_csv('3-contagem_empresas_por_municipio2.csv', index=False)

# Salvar as alterações de volta no arquivo CSV
data.to_csv('3-result_residuossolidos_ate2012_atm.csv', index=False)


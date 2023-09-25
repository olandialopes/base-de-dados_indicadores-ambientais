import pandas as pd

data = pd.read_csv('3-relatorio residuos solidos_ibama_ate 2012.csv', delimiter=';')

# Contar valores únicos na coluna CNPJ (quantidade de CNPJ na base de dados)
contagem_valores_CNPJ = data['CNPJ do gerador'].nunique()
contagem_valores_municipios = data['Município'].nunique()
# Imprimir a contagem de valores únicos
print(f'Quantidade de CNPJ da base original: {contagem_valores_CNPJ}')
print(f'Quantidade de municipios da base original: {contagem_valores_municipios}')

# Colunas a serem excluidas
variaveis_excluidas = [
    'Código da Categoria', 'Categoria de Atividade', 'Código do Detalhe', 'Detalhe', 'Cod. Resíduo', 'Tipo de Resíduo',
    'Tipo de monit. realizado', 'Tipo de Finalidade', 'Finalidade da Transferência', 'CNPJ da emp. de Armazen/Destin',
    'Raz. soc. emp. Armazen/Destin', 'Latitude', 'Longitude', 'Situação Cadastral',
    'Identif. do Resíduo NBR 10.004', 'Efic. do sist. de tratamento'

]
# Excluir as variáveis excluidas, cujos nomes estão acima
data = data.drop(columns=variaveis_excluidas, axis=1)

# Excluir linhas com pelo menos uma célula vazia em qualquer coluna
data = data.dropna(how='any')

# Contar valores únicos na coluna CNPJ (quantidade de CNPJ na base de dados)
contagem_valores_CNPJ = data['CNPJ do gerador'].nunique()
contagem_valores_municipios = data['Município'].nunique()
# Imprimir a contagem de valores únicos
print(f'Quantidade de CNPJ depois de excluir qualquer celula em branco: {contagem_valores_CNPJ}')
print(f'Quantidade de municipios depois de excluir qualquer celula em branco:: {contagem_valores_municipios}')

# Excluir linhas com valores zero em qualquer coluna
data = data[~(data == '0').any(axis=1)]

# Contar valores únicos na coluna CNPJ (quantidade de CNPJ na base de dados)
contagem_valores_CNPJ = data['CNPJ do gerador'].nunique()
contagem_valores_municipios = data['Município'].nunique()
# Imprimir a contagem de valores únicos
print(f'Quantidade de CNPJ depois de excluir qualquer celula valor igual a zero: {contagem_valores_CNPJ}')
print(f'Quantidade de municipios depois de excluir qualquer celula valor igual a zero: {contagem_valores_municipios}')

# Contar valores únicos na coluna muncípio (quantidade de municípios na base de dados)
contagem_valores_unicos = data['Município'].nunique()

# Salvar as alterações de volta no arquivo CSV
data.to_csv('3-result_residuossolidos_ate2012_atm.csv', index=False)

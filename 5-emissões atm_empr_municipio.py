import pandas as pd

data = pd.read_csv('5-relatorio_emissoes atmosfericas ibama.csv', delimiter=';')

# Colunas a serem excluidas
variaveis_excluidas = [
'Código da Categoria','Categoria de Atividade','Código do Detalhe','Detalhe', 'Observações',
'Situação Cadastral', 'Densidade','Unidade de Medida - densidade', 'Justificativa para alteração da densidade',
'Poder Calorífico Inferior', 'Unidade de Medida - Poder Calorífico Inferior',
'Justificativa para alteração do Poder Calorífico Inferior',
'Justificativa para Alteração do Conteúdo de Carbono', 'Fator de Oxidação',
'Unidade de Medida - Fator de Oxidação',
'Justificativa para Alteração do Fator de Oxidação', 'Conteúdo de Carbono', 'Unidade de Medida - Conteúdo de Carbono'
]
#Excluir as variáveis excluidas, cujos nomes estão acima
data = data.drop(columns=variaveis_excluidas, axis=1)


# Contar valores únicos de CNPJ em cada município
contagem_empresas_por_municipio = data.groupby('Município')['CNPJ'].nunique()

# Contar quantas vezes cada município aparece
contagem_municipios = data['Município'].value_counts().reset_index()
contagem_municipios.columns = ['Município', 'Quantidade de Empresas']
# Salvar a contagem em um arquivo CSV
contagem_municipios.to_csv('5-contagem_empresas_por_municipio.csv', index=False)

# Excluir linhas com pelo menos uma célula vazia em qualquer coluna
data = data.dropna(how='any')

# Contar valores únicos de CNPJ em cada município
contagem_empresas_por_municipio = data.groupby('Município')['CNPJ'].nunique()
# Contar quantas vezes cada município aparece
contagem_municipios = data['Município'].value_counts().reset_index()
contagem_municipios.columns = ['Município', 'Quantidade de Empresas']
# Salvar a contagem em um arquivo CSV
contagem_municipios.to_csv('5-contagem_empresas_por_municipio2.csv', index=False)

# Excluir linhas com valores zero em qualquer coluna
data = data[~(data == '0').any(axis=1)]

# Contar valores únicos de CNPJ em cada município
contagem_empresas_por_municipio = data.groupby('Município')['CNPJ'].nunique()
# Contar quantas vezes cada município aparece
contagem_municipios = data['Município'].value_counts().reset_index()
contagem_municipios.columns = ['Município', 'Quantidade de Empresas']
# Salvar a contagem em um arquivo CSV
contagem_municipios.to_csv('5-contagem_empresas_por_municipio2.csv', index=False)

# Salvar as alterações de volta no arquivo CSV
data.to_csv('5-result_emissoes_atm.csv', index=False)

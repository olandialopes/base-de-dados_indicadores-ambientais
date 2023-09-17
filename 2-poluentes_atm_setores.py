import pandas as pd

data = pd.read_csv('2-poluentes atmosfericos_dados_ibama.csv', delimiter=';')

# Colunas a serem excluidas
variaveis_excluidas = [
    'Código da Categoria', 'Código do Detalhe', 'Detalhe',
    'Metodologia utilizada', 'Situação Cadastral'
]
#Excluir as variáveis excluidas, cujos nomes estão acima
data = data.drop(columns=variaveis_excluidas, axis=1)


# Contar valores únicos de CNPJ em cada setor
contagem_empresas_por_setor = data.groupby('Categoria de Atividade')['CNPJ'].nunique()

# Contar quantas vezes cada município aparece
contagem_setor = data['Categoria de Atividade'].value_counts().reset_index()
contagem_setor.columns = ['Categoria de Atividade', 'Quantidade de Empresas']
# Salvar a contagem em um arquivo CSV
contagem_setor.to_csv('2-contagem_empresas_por_setor.csv', index=False)

# Excluir linhas com pelo menos uma célula vazia em qualquer coluna
data = data.dropna(how='any')

# Contar valores únicos de CNPJ em cada município
contagem_empresas_por_setor = data.groupby('Categoria de Atividade')['CNPJ'].nunique()
# Contar quantas vezes cada município aparece
contagem_setor = data['Categoria de Atividade'].value_counts().reset_index()
contagem_setor.columns = ['Categoria de Atividade', 'Quantidade de Empresas']
# Salvar a contagem em um arquivo CSV
contagem_setor.to_csv('2-contagem_empresas_por_setor2.csv', index=False)

# Excluir linhas com valores zero em qualquer coluna
data = data[~(data == '0').any(axis=1)]

# Contar valores únicos de CNPJ em cada setor
contagem_empresas_por_setor = data.groupby('Categoria de Atividade')['CNPJ'].nunique()
# Contar quantas vezes cada setor aparece
contagem_setor = data['Categoria de Atividade'].value_counts().reset_index()
contagem_setor.columns = ['Categoria de Atividade', 'Quantidade de Empresas']
# Salvar a contagem em um arquivo CSV
contagem_setor.to_csv('2-contagem_empresas_por_setor3.csv', index=False)

# Salvar as alterações de volta no arquivo CSV
data.to_csv('2-result_poluentes_atm_setor.csv', index=False)


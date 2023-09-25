import pandas as pd

data = pd.read_csv('1-relatorio efluentes liquidos_ibama.csv', delimiter=';')

# Colunas a serem excluidas
colunas_indesejadas = [
    'Código da Categoria', 'Código do Detalhe', 'Desc. Monitoramento Utilizado',
    'Compart. Ambiental da Emissão', 'Tipo de Emissão', 'Tipo Corpo Receptor',
    'Classe do Corpo Receptor', 'Nome do Corpo Hídrico', 'Corpo Receptor',
    'Qual?', 'Empresa Receptora do Efluente', 'Tipo de Emissão Para o Solo',
    '(Se outro) Qual?', 'Situação Cadastral','Latitude','Longitude',
    'Tipo de Tratamento', 'Nível de Tratamento', 'Detalhe'
]
# Excluir as colunas indesejadas, cujos nomes estão acima
data = data.drop(columns=colunas_indesejadas, axis=1)

# Contar valores únicos de CNPJ por setor econômico
contagem_empresas_por_setor = data.groupby('Categoria de Atividade')['CNPJ'].nunique()

# Contar quantas vezes cada setor aparece
contagem_setor = data['Categoria de Atividade'].value_counts().reset_index()
contagem_setor.columns = ['Categoria de Atividade', 'Quantidade de Empresas']
# Salvar a contagem em um arquivo CSV
contagem_setor.to_csv('contagem_empresas_por_setor.csv', index=False)

# Excluir linhas com pelo menos uma célula vazia em qualquer coluna
data = data.dropna(how='any')

# Contar valores únicos de CNPJ por setor econômico
contagem_empresas_por_setor = data.groupby('Categoria de Atividade')['CNPJ'].nunique()
# Contar quantas vezes cada município aparece
contagem_setor = data['Categoria de Atividade'].value_counts().reset_index()
contagem_setor.columns = ['Categoria de Atividade', 'Quantidade de Empresas']
# Salvar a contagem em um arquivo CSV
contagem_setor.to_csv('contagem_empresas_por_setor2.csv', index=False)

# Excluir linhas com valores zero em qualquer coluna
data = data[~(data == '0').any(axis=1)]

# Contar valores únicos de CNPJ em cada município
contagem_empresas_por_municipio = data.groupby('Categoria de Atividade')['CNPJ'].nunique()
# Contar quantas vezes cada município aparece
contagem_municipios = data['Categoria de Atividade'].value_counts().reset_index()
contagem_municipios.columns = ['Categoria de Atividade', 'Quantidade de Empresas']
# Salvar a contagem em um arquivo CSV
contagem_municipios.to_csv('contagem_empresas_por_setor3.csv', index=False)

# Salvar as alterações de volta no arquivo CSV
data.to_csv('1-result_efluentes liquidos_emp_setor.csv', index=False)


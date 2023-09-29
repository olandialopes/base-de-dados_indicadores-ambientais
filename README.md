# Dados base análise indicadores poluição por setores CNAE

Este repositório lê e organiza bases disponíveis no IBAMA :
1. Resíduos sólidos e líquidos
2. Poluentes e emissões atmosféricas

Organizado por Olandia Lopes, Valdex de Jesus Santos e Bernardo Alves Furtado

## How to run

1. Com as bases no diretório original_data e a path indicada na variável **f0**, simplesmente run `python wrangling_databases.py`
2. Os resultados são as cinco bases limpas, organizadas em um dicionário e uma lista de CNPJs e Anos

# RESULTADOS DAS BASES

Base 1: 
## Efluentes líquidos

Indicadores: Quantidade gerada de efluentes líquidos por ano e por empresa/setor e eficiência do tratamento;

Base de dados 2: 
## Emissões atmosféricas

- Indicadores:

·         Quantidade gerada de poluentes atmosféricos (Material particulado - MP) por ano e por empresa/setor;

·         Quantidade gerada de poluentes atmosféricos (Monóxido de carbono – CO)) por ano e por empresa/setor

·         Quantidade gerada de poluentes atmosféricos (Óxidos de nitrogênio – NOx) por ano e por empresa/setor

·         Quantidade gerada de poluentes atmosféricos (Óxidos de enxofre – SOx) por ano e por empresa/setor


Base de dados 3 e 4
## Resíduos sólidos 

- Indicador:

·         Quantidade gerada de resíduos sólidos por classe (perigoso e não perigoso) por ano e por empresa/setor;


Base de dados 5: 
## Emissões atmosféricas 

- Indicadores

·         Quantidade consumida de energia por tipo de fonte energética (eletricidade – rede pública; biomassa-lenha; turfa; óleo diesel, entre outros ) por ano e por empresa/setor;

·         Quantidade de emissões de CO2 por ano, por empresa/setor.

## Sources:
Os dados utilizados foram coletados da base de dados do IBAMA disponíveis no Relatório Anual de Atividades Potencialmente Poluidoras e Utilizadoras de Recursos Ambientais – RAPP, conforme abaixo:

1. Efluentes liquidos: https://dadosabertos.ibama.gov.br/pt_PT/dataset/efluentes-liquidos
2. Emissões de Poluentes atmosféricos: https://dadosabertos.ibama.gov.br/pt_PT/dataset/emissoes-de-poluentes-atmosfericos
3. Resíduos sólidos anterior a 2012: https://dadosabertos.ibama.gov.br/pt_PT/dataset/residuos-solidos-gerador-anterior-a-2012
4. Resíduos sólidos a partir de 2012: https://dadosabertos.ibama.gov.br/pt_PT/dataset/residuos-solidos-gerador-a-partir-de-2012
5. Emissões atmosféricas: https://dadosabertos.ibama.gov.br/pt_PT/dataset/fontes-energeticas



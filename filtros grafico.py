# organização dos códigos referentes aos filtros para TD
# grafico 1 TD - residuos solidos acima de 1 tonelada - setor realestate
# para filtrar base
g1= b['residuos_solidos2'][(b['residuos_solidos2']['quant_tonelada']>1)&(b['residuos_solidos2']['isic_12']=='RealEstate')&(b['residuos_solidos2']['ano']>2011)]
sns.boxplot(data=g1,x='ano', y='quant_tonelada', whis=(0,100))
plt.show()
# grafico 2 TD - residuos solidos acima de 26000 toneladas- setor transport

g2= b['residuos_solidos2'][(b['residuos_solidos2']['quant_tonelada']>26000)&(b['residuos_solidos2']['isic_12']=='Transport')]
sns.boxplot(data=g2,x='ano', y='quant_tonelada', whis=(0,100))
plt.show()
# grafico 3 TD - residuos solidos acima de 26000 toneladas- setor trade

g3= b['residuos_solidos2'][(b['residuos_solidos2']['quant_tonelada']>26000)&(b['residuos_solidos2']['isic_12']=='Trade')]
sns.boxplot(data=g3,x='ano', y='quant_tonelada', whis=(0,100))
plt.show()

# grafico 4 TD - poluentes atmosféricos por setores econômicos acima de zero
g4= b['poluentes_atm'][(b['poluentes_atm']['quant_poluentes_emitidos']>0)]
sns.boxplot(data=g4,x='isic_12', y='quant_poluentes_emitidos', whis=(0,100))
plt.xticks(rotation=90)
plt.tight_layout(pad=2.0)
plt.show()

# Gráfico 5 a 9 TD -  poluentes atmosféricos por setores econômicos e por região (valores acima de zero)

# Região Sudeste

g5= b['poluentes_atm'][(b['poluentes_atm']['quant_poluentes_emitidos']>0)&(b['poluentes_atm']['region'] == 'Sudeste')]
sns.boxplot(data=g5,x='isic_12', y='quant_poluentes_emitidos', whis=(0,100))
plt.xticks(rotation=90)
plt.tight_layout(pad=2.0)
plt.show()
# Região Norte
g6= b['poluentes_atm'][(b['poluentes_atm']['quant_poluentes_emitidos']>0)&(b['poluentes_atm']['region'] == 'Norte')]
sns.boxplot(data=g6,x='isic_12', y='quant_poluentes_emitidos', whis=(0,100))
plt.xticks(rotation=90)
plt.tight_layout(pad=2.0)
plt.show()

# região Sul

g7= b['poluentes_atm'][(b['poluentes_atm']['quant_poluentes_emitidos']>0)&(b['poluentes_atm']['region'] == 'Sul')]
sns.boxplot(data=g7,x='isic_12', y='quant_poluentes_emitidos', whis=(0,100))
plt.xticks(rotation=90)
plt.tight_layout(pad=2.0)
plt.show()

# região Centro-oeste

g8= b['poluentes_atm'][(b['poluentes_atm']['quant_poluentes_emitidos']>0)&(b['poluentes_atm']['region'] == 'Centro-oeste')]
sns.boxplot(data=b9,x='isic_12', y='quant_poluentes_emitidos', whis=(0,100))
plt.xticks(rotation=90)
plt.tight_layout(pad=2.0)
plt.show()

# região Nordeste
g9= b['poluentes_atm'][(b['poluentes_atm']['quant_poluentes_emitidos']>0)&(b['poluentes_atm']['region'] == 'Nordeste')]
sns.boxplot(data=g9,x='isic_12', y='quant_poluentes_emitidos', whis=(0,100))
plt.xticks(rotation=90)
plt.tight_layout(pad=2.0)
plt.show()

# gráfico 10 TD - emissoes de CO2 acima de zero região Norte
g10= b['emissoes'][(b['emissoes']['co2_emissions']>0)&(b['emissoes']['region'] == 'Norte')]
sns.boxplot(data=g10,x='isic_12', y='co2_emissions', whis=(0,100))
plt.xticks(rotation=90)
plt.tight_layout(pad=2.0)
plt.show()
# gráfico 11 TD - emissoes de CO2 acima de zero região centro-oeste
# Região centro-oeste

g11= b['emissoes'][(b['emissoes']['co2_emissions']>0)&(b['emissoes']['region'] == 'Centro-oeste')]
sns.boxplot(data=g11,x='isic_12', y='co2_emissions', whis=(0,100))
plt.xticks(rotation=90)
plt.tight_layout(pad=2.0)
plt.show()

# Região Nordeste
g12= b['emissoes'][(b['emissoes']['co2_emissions']>0)&(b['emissoes']['region'] == 'Nordeste')]
sns.boxplot(data=g12,x='isic_12', y='co2_emissions', whis=(0,100))
plt.xticks(rotation=90)
plt.tight_layout(pad=2.0)
plt.show()

# Região Sudeste
g13= b['emissoes'][(b['emissoes']['co2_emissions']>0)&(b['emissoes']['region'] == 'Sudeste')]
sns.boxplot(data=g13,x='isic_12', y='co2_emissions', whis=(0,100))
plt.xticks(rotation=90)
plt.tight_layout(pad=2.0)
plt.show()

# grafico 14 TD - indicador eficiência de tratamento de efluentes por setor econômico (valores >0 e <100)

g14= b['efluentes'][(b['efluentes']['perc_efficiency_treatment']>0)&(b['efluentes']['perc_efficiency_treatment']<100)]
sns.boxplot(data=g14,x='isic_12', y='co2_emissions', whis=(0,100))
sns.boxplot(data=b9,x='isic_12', y='perc_efficiency_treatment', whis=(0,100))
plt.xticks(rotation=90)
plt.tight_layout(pad=2.0)
plt.show()







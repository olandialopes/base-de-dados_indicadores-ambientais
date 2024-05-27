import geobr
import matplotlib.pyplot as plt

regions = geobr.read_region(year=2010)
fig, ax = plt.subplots(figsize=(4, 4), dpi=200)   

regions.plot(facecolor='#B7E4DB', edgecolor='#f0d172', ax=ax)

ax.set_title('Ecoeficiência (2010)', fontsize=16)
ax.axis('off')

plt.show()
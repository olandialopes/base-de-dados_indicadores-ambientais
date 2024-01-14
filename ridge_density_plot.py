import seaborn as sns
import matplotlib.pyplot as plt


def draw_density_plot(base, key, y_seq_lines, col):
    # Initialize the FacetGrid object
    pal = sns.color_palette(palette='coolwarm', n_colors=len(y_seq_lines))
    g = sns.FacetGrid(base[key], row=y_seq_lines, hue=y_seq_lines, aspect=15, height=.5, palette=pal)

    # Draw the densities in a few steps
    g.map(sns.kdeplot, col,
          bw_adjust=.5, clip_on=False,
          fill=True, alpha=1, linewidth=1.5)
    g.map(sns.kdeplot, col, clip_on=False, color="w", lw=2, bw_adjust=.5)

    # passing color=None to refline() uses the hue mapping
    g.refline(y=0, linewidth=2, linestyle="-", color=None, clip_on=False)

    # Set the subplots to overlap
    g.figure.subplots_adjust(hspace=-.25)

    # Remove axes details that don't play well with overlap
    g.set_titles("")
    g.set(yticks=[], ylabel="")
    g.despine(bottom=True, left=True)
    plt.show()

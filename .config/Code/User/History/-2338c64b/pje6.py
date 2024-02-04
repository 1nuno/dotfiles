import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from matplotlib.widgets import Slider


def groupby_numpy(array, groupby=-1):
    labels = np.unique(array[:, groupby], return_index=True)
    return labels[0],np.split(array[:,:groupby], labels[1][1:])

def detecta_outlier_zscore(array,k=3):
    mean = array.mean()
    std = array.std() 
    outliers = []
    index = []
    for c,i in enumerate(array): 
        z = abs((i-mean)/std)
        if z > k: 
            outliers.append(i)
            index.append(c)
    return outliers


dados = np.load('dados_estruturados.npy')
dados_emocoes = np.delete(dados, -2, 1)
labels,dados_por_emocoes = groupby_numpy(dados_emocoes)
target='y_5'
grouped_data = dados_por_emocoes
k = 3

if target == '':
    column = 0
    target = 'x_0'
else:
    column = int(target.split('_')[-1])
    coordinate = target.split('_')[0]

    if coordinate == 'y':
        column += 68

bg_color = 'xkcd:midnight'
other_color = 'xkcd:lightblue'
colors = [
            'xkcd:lightblue',
            'xkcd:carolina blue',
            'xkcd:greeny blue',
            'xkcd:blue grey',
            'xkcd:dark salmon',
            'xkcd:twilight blue',
            'xkcd:royal purple',
            'xkcd:light tan',
            ]

data = [i[:,column] for i in grouped_data]

fig, (ax,ax1) = plt.subplots(figsize=(14,10),
                             nrows=2,
                             gridspec_kw=dict(height_ratios=[10,1],
                                              hspace=1))
fig.set_facecolor(bg_color)
ax.set_facecolor(bg_color)
ax.tick_params(axis='x', colors=bg_color,pad=20,size=10)
ax.tick_params(axis='y', colors=other_color,pad=20,size=10)
ax.spines['bottom'].set_color(bg_color)
ax.spines['left'].set_color(bg_color)
ax.spines['top'].set_color(bg_color)
ax.spines['right'].set_color(bg_color)

plotted = ax.boxplot(
                        data,
                        patch_artist=True,
                        widths=0.3,
                        medianprops={"color":"white",
                                    "linewidth": 0.5},
                        boxprops={"facecolor": other_color,
                                "edgecolor": "white",
                                "linewidth": 0.5},
                        whiskerprops={"color": other_color,
                                    "linewidth": 1.5},
                        capprops={"color": other_color},
                        flierprops={'marker':'o',
                                    'markerfacecolor':'xkcd:dull red',
                                    'markersize':9,
                                    'linestyle':'none',
                                    'markeredgecolor':'xkcd:sky',
                                    'linewidth':1}, zorder=1)

ax.set_xticks([1,2,3,4,5,6,7,8], ['😶','😇 ','😁','😢','😡','😨','😾','😱',],fontsize=40)
ax.set_xlabel('Emoções',fontsize=12, labelpad=20,color=other_color)
ax.set_ylabel(f'coordenadas {target}',fontsize=12,labelpad=20,color=other_color)

for i,v in enumerate(ax.get_xticklabels()):
    v.set_color(colors[i])

caps = plotted['caps']
caps = [caps[n:n+2] for n in range(0, len(caps), 2)]
boxes = plotted['boxes']
for i,items in enumerate(zip(caps,boxes)):
    cap, box = items
    box.set(facecolor=colors[i])
    for j in range(2):
        cap[j].set(xdata=cap[j].get_xdata() + (-0.025,0.025), linewidth=2)
    
    
ax.set_xlim([0,9])
ax.set_title('Boxplot de emoções', fontsize=15, pad=100,color=other_color)

slider = Slider(ax1, "K", valmin=0, valmax=15)
slider.valtext.set_color(other_color)
slider.label.set_color(other_color)
slider.label.set_size(20)

def update(val):
    ax.clear()
    ax.set_facecolor(bg_color)
    ax.tick_params(axis='x', colors=bg_color,pad=20,size=10)
    ax.tick_params(axis='y', colors=other_color,pad=20,size=10)
    ax.spines['bottom'].set_color(bg_color)
    ax.spines['left'].set_color(bg_color)
    ax.spines['top'].set_color(bg_color)
    ax.spines['right'].set_color(bg_color)
    plotted = ax.boxplot(
                            data,
                            patch_artist=True,
                            widths=0.3,
                            medianprops={"color":"white",
                                        "linewidth": 0.5},
                            boxprops={"facecolor": other_color,
                                    "edgecolor": "white",
                                    "linewidth": 0.5},
                            whiskerprops={"color": other_color,
                                        "linewidth": 1.5},
                            capprops={"color": other_color},
                            flierprops={'marker':'o',
                                        'markerfacecolor':'xkcd:dull red',
                                        'markersize':9,
                                        'linestyle':'none',
                                        'markeredgecolor':'xkcd:sky',
                                        'linewidth':1}, zorder=1)
    
    ax.set_xticks([1,2,3,4,5,6,7,8], ['😶','😇 ','😁','😢','😡','😨','😾','😱',],fontsize=40)
    ax.set_xlabel('Emoções',fontsize=12, labelpad=20,color=other_color)
    ax.set_ylabel(f'coordenadas {target}',fontsize=12,labelpad=20,color=other_color)

    for i,v in enumerate(ax.get_xticklabels()):
        v.set_color(colors[i])

    fliers = plotted['fliers']
    caps = plotted['caps']
    caps = [caps[n:n+2] for n in range(0, len(caps), 2)]
    boxes = plotted['boxes']
    for i,items in enumerate(zip(caps,boxes)):
        cap, box = items
        box.set(facecolor=colors[i])
        for j in range(2):
            cap[j].set(xdata=cap[j].get_xdata() + (-0.025,0.025), linewidth=2)

        x = fliers[i].get_xdata()
        y = fliers[i].get_ydata()
        outliers = detecta_outlier_zscore(y,k=val)
        if outliers:
            x = x[:len(outliers)]
            ax.scatter(x,outliers,s=75, facecolors='xkcd:fluro green', linewidth=2, edgecolors='red', zorder=1+i)



    # for i in range(8):
    #     x = fliers[i].get_xdata()
    #     y = fliers[i].get_ydata()
    #     outliers = detecta_outlier_zscore(y,k=val)
    #     if outliers:
    #         x = x[:len(outliers)]
    #         ax.scatter(x,outliers,s=75, facecolors='xkcd:fluro green', linewidth=2, edgecolors='red', zorder=1+i)
    ax.set_xlim([0,9])
    ax.set_title('Boxplot de emoções', fontsize=15, pad=100,color=other_color)
slider.on_changed(update)
plt.show()

# dados = get_dados_estruturados(dimensao='2d',orderby='emocao')
# dados = np.load('dados_estruturados.npy')
# dados_emocoes = np.delete(dados, -2, 1)
# labels,dados_por_emocoes = groupby_numpy(dados_emocoes)
# np.save('dados_por_emocoes.npy', dados_por_emocoes)
# plot_boxplot_zscore(dados_por_emocoes,target='y_5',k=3)



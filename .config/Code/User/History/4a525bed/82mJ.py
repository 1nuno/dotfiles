import numpy as np
from sklearn.cluster import KMeans,DBSCAN
import matplotlib.pyplot as plt


def plot_kmeans(dados_normalizados,label,p=0,clusters=8,eps=6,min=3):
    x = p
    y = p + 68
    X = np.array(list(zip(dados_normalizados[:,x],dados_normalizados[:,y])))
    kmeans = KMeans(n_clusters=clusters, random_state=0, n_init="auto").fit(X)
    # clustering = DBSCAN(eps=eps, min_samples=min).fit(X)
    
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

    fig,ax = plt.subplots(figsize=(8,8))
    fig.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)
    ax.tick_params(axis='x', colors=other_color,pad=20,size=10)
    ax.tick_params(axis='y', colors=other_color,pad=20,size=10)
    ax.spines['bottom'].set_color(bg_color)
    ax.spines['left'].set_color(bg_color)
    ax.spines['top'].set_color(bg_color)
    ax.spines['right'].set_color(bg_color)
    ax.scatter(X[:,0],X[:,1],c=kmeans.labels_, cmap='jet')
    # ax.scatter(X[:,0],X[:,1])
    plt.show()

def detecta_outlier_zscore(array,k=3):
    mean = np.mean(array)
    std = np.std(array) 
    outliers = []
    for i in array: 
        z = abs((i-mean)/std)
        if z > k: 
            outliers.append(i)
    return outliers

def inject_outliers(array,x,k=3,iter=20):
    print(array)
    outliers = detecta_outlier_zscore(array,k=k)
    density = round(len(outliers)/len(array),2)*100
    print(f'initial density: {density}')
    for i in range(iter):
        if density < x:
            add_density = x-density
            sample = []
            for i in array:
                if i not in outliers:
                    sample.append(i)
                    array.remove(i)
                    if round(len(sample)/len(array),2)*100 >= add_density:
                        break
            for i in sample:
                mean = np.mean(array)
                std = np.std(array)
                s = np.random.choice([-1,1])
                q = s*(mean+k*std)
                p = mean + s*k*std + q
                array.append(p)
            
            outliers = detecta_outlier_zscore(array,k=k)
            density = round(len(outliers)/len(array),2)*100
            print(f'current density: {density}')

dados = np.load('dados_estruturados.npy')
label = dados[:,-1]
plot_kmeans(dados,label,p=30,clusters=8,eps=4,min=10)

def idade_count(idades):
    print(len(idades))

def idade_display(idades):
    print(idades)

def idade_display_inv(idades):
    print(idades[::-1])

def idade_display_2(idades):
    print(idades[1:-1])

def idade_display_min_max(idades):
    print(f'{min(idades)} - {max(idades)}')

def idade_sum(idades):
    print(sum(idades))

def idade_ref(idades,ref):
    print([i for i in idades if i < ref])

def idade_17(idades):
    print(17 in idades)

def remove_aluno(nomes,idades,x):
    return nomes[:x] + nomes[x+1:], idades[:x] + idades[x+1:]

def remove_aluno(nomes,idades,x):
    return nomes[:x] + nomes[x+1:], idades[:x] + idades[x+1:]

def remove_aluno(idades,x):
    return idades[x]

if __name__ == '__main__':
    idades = [10,1,12,17,13,22,50,80]
    idade_count(idades)
    idade_display(idades)
    idade_display_inv(idades)
    idade_display_2(idades)
    idade_display_min_max(idades)
    idade_sum(idades)
    idade_ref(idades,30)
    idade_17(idades)
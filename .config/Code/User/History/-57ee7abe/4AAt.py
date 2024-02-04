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
    if 17 in idades:
        return True
    return False

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
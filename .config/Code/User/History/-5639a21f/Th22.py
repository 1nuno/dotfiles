

#8.6
def compute_metabolism(data):
    return {i:(66 + 6.3*j[-1] + 12.9*j[2] - 6.8*j[1]) if j[0] == 'm' else (655 + 4.3*j[-1] + 4.7*j[2]- 4.7*j[1]) for i,j in data.items()}

#8.7
def compute_massa_corporal(data):
    return {i:[j[0],j[1],j[0]/j[1]**2] for i,j in data.items()}

def inverte_dict(dic):
    res = {}
    for key, val in dic.items():
        res.setdefault(val, key)
    return {j:i for i,j in dic.items()}

# print(compute_metabolism({'jsdkj': ['f',15,1.60,60]}))
print(compute_massa_corporal({'jsdkj': [60,1,60]}))
# print(inverte_dict({'carro': 'ssssssss','c':'ssssssss'}))


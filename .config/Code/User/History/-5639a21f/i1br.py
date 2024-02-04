

#8.6
def compute_metabolism(data):
    return {i:(66 + 6.3*j[-1] + 12.9*j[2] - 6.8*j[1]) if j[0] == 'm' else (655 + 4.3*j[-1] + 4.7*j[2]- 4.7*j[1]) for i,j in data.items()}

#8.7
def compute_massa_corporal(data):
    return {i:[j[0],j[1],j[0]/j[1]**2] for i,j in data.items()}

#8.11
def is_balanced(color):
    return list(color.values())[0] == list(color.values())[1] == list(color.values())[2]

#8.13
def concatenate_dict(dict1,dict2):
    final_dict = dict1.copy()
    for i,j in dict2.items():
        if i not in final_dict:
            final_dict[i] = j
        elif isinstance(final_dict[i], list):
            final_dict[i].append(j)
        else:
            final_dict[i] = [final_dict[i],j]
    return final_dict

#8.14
def find_min_prob(probs):
    return list(probs.keys())[list(probs.values()).index(min(probs.values()))]



# print(compute_metabolism({'jsdkj': ['f',15,1.60,60]}))
# print(compute_massa_corporal({'jsdkj': [60,1.60]}))
print(is_balanced({'R':0,'G':0,'B':1}))
# print(concatenate_dict({'A':2},{'B':3,'A':3}))
# print(find_min_prob({'A':2,'B':4,'C':1}))
# print(inverte_dict({'carro': 'ssssssss','c':'ssssssss'}))


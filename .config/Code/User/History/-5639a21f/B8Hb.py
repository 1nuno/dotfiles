def compute_metabolism(data):
    return {i:(66 + 6.3*j[-1] + 12.9*[2] - 6.8*j[1]) if j[0] == 'm' else (655 + 4.3*j[-1] + 4.7*j[2]- 4.7*j[1]) for i,j in data.items()}

compute_metabolism({'jsdkj': ['m',15,1.60,60]})
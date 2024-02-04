def compute_metabolism(data):
    return {i:(66 + 6.3*j[-1] + 12.9*[2]) if j[0] == 'm' else (66 + 6.3*j[-1] + 12.9*[2]) for i,j in data.items()}
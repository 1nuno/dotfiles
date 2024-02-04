import matplotlib.pyplot as plt

# 9.10
def count_char(file_name):
    with open(file_name, 'r') as file:
         char_count = {}
         for c in file.read():
            char_count[c] = char_count.get(c,0) + 1
    return char_count

# 9.10
def plot_frequencies(count_char):
    fig, ax = plt.subplots()
    ax.bar(list(count_char.keys()), list(count_char.values()))
    ax.set_ylabel('Chars')
    ax.set_title('Char frequency')
    plt.show()





if __name__ == '__main__':
    # 9.10
    plot_frequencies(count_char('hello_mom.txt'))

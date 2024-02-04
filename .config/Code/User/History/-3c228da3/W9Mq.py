import matplotlib.pyplot as plt

def count_char(file_name):
    with open(file_name, 'r') as file:
         char_count = {}
         for c in file.read():
            if c not in char_count:
                char_count[c] = 1
            else:
                char_count[c] = char_count[c] + 1
    return char_count

def plot_frequencies(count_char):
    fig, ax = plt.subplots()
    ax.bar(list(count_char.keys()), list(count_char.values()))
    ax.set_ylabel('Chars')
    ax.set_title('Char frequency')
    plt.show()


if __name__ == '__main__':
    plot_frequencies(count_char('hello_mom.txt'))


def byte_pair_encoding(training_data, test_data):
    unique_chars_in_training_data = set(training_data)
    current_pos = 0
    occurences = {}
    for i in range(-1,len(training_data),2):
        if (training_data[i-1], training_data[i]) not in occurences:
            occurences[(training_data[i-1], training_data[i])] = 1
        else:
            occurences[(training_data[i-1], training_data[i])] += 1
            





if __name__ == "__main__":
    training_data = "low low low low low lowest lowest newer newer newer newer newer newer wider wider wider new new"
    test_data = "newer"
    result = byte_pair_encoding(training_data, test_data)

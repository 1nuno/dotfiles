def byte_pair_encoding_learner(training_data):
    training_data = list(training_data)    
    max_occurences_pairs = []
    max_occurences = 1
    for k in range(8):
        occurences = {}
        for i in range(1, len(training_data)):
            if (training_data[i - 1], training_data[i]) not in occurences:
                occurences[(training_data[i - 1], training_data[i])] = [1, [i-1]]
            else:
                occurences[(training_data[i - 1], training_data[i])][0] += 1
                occurences[(training_data[i - 1], training_data[i])][1].append(i-1)  

            if occurences[(training_data[i - 1], training_data[i])][0] > max_occurences:
                max_occurences = occurences[(training_data[i - 1], training_data[i])][0]
                max_occurences_pair = (training_data[i-1], training_data[i])

        max_occurences_pairs.append(max_occurences_pair)
        print(occurences.keys())
        for i in occurences[max_occurences_pair][1][::-1]:
            training_data[i] = training_data[i] + training_data[i+1]
            del training_data[i+1]
    return max_occurences_pairs

def byte_pair_encoding_segmenter(max_occurences_pairs,test_data):
    test_data = list(test_data)
    test_data_pairs = []
    for i in range(1, len(test_data)):
        if (test_data[i - 1], test_data[i]) not in test_data_pairs:
            test_data_pairs.append((test_data[i - 1], test_data))
    pairs_intersection = set(test_data_pairs).intersection(set(max_occurences_pairs))
    for pair in pairs_intersection:
        for i in range(len(test_data),1,-1):
            if (test_data[i - 1], test_data[i]) == pair:
                test_data[i-1] = test_data[i - 1] + test_data[i]
                del test_data[i]
    return test_data

if __name__ == "__main__":
    training_data = "low low low low low lowest lowest newer newer newer newer newer newer wider wider wider new new"
    test_data = "newer"
    max_occurences_pairs = byte_pair_encoding_learner(training_data)
    result = byte_pair_encoding_segmenter(max_occurences_pairs, test_data)
    print(result)


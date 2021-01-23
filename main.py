def save_weighs():
    my_file = open("weights.txt", 'w')
    temp_W = []
    for i in range(len(W)):
        one_str = str(W[i]).replace('], [', ':').replace('[', '').replace(']', '').replace(': ', ':').replace(',',
                                                                                                              '').replace(
            'array', '').replace('(', '').replace(')', '').replace('\n', ':')
        if i != (len(W) - 1):
            one_str = one_str + '\n'
        temp_W.append(one_str)
    my_file.writelines(temp_W)
    my_file.close()


def load_weights():
    global W
    W = []
    my_file = open("weights.txt", 'r')
    one_line = my_file.read().split('\n')
    for i in range(len(one_line)):
        W1 = []
        two_line = one_line[i].split(':')
        for j in range(len(two_line)):
            W2 = []
            three_line = two_line[j].split(' ')
            for k in range(len(three_line)):
                if three_line[k] != '':
                    W2.append(float(three_line[k]))
            W1.append(W2)
        # W.append(W1)
        W.append([])
        W[i] = np.array(W1)
        outs.append([])
    my_file.close()

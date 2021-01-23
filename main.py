
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



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


if __name__ == '__main__':
    l1 = 0
    while l1 != 1 and l1 != 2:
        print("От куда загрузить веса для нейросети")
        print("1) Файл")
        print("2) Сгенерировать")
        l1 = int(input("Выберите действие"))
    if l1 == 1:
        print("Загрузка нейросети из файла")
        load_weights()
    if l1 == 2:
        random_weighs()
        print("Веса сгенерированы")

    l2 = 0
    while l2 != 3:
        print("1) Обучить нейросеть")
        print("2) Найти по ключевым словам УДК")
        print("3) Выйти")
        l2 = int(input("Выберите действие"))
        if l2 == 1:
            print("Обучение")
            load_data()  # загрузка данных для обучения из файла
            train(epoch)
            l3 = 0
            while l3 != 4:
                print("Выберите дейчтвие")
                print("1) Сохранить веса")
                print("2) Сбросить веса")
                print("3) Повторить обучение")
                print("4) Выйти в главное меню")
                l3 = int(input("Выберите действие"))
                if l3 == 1:
                    print("Сохранение весов")
                    save_weighs()
                if l3 == 2:
                    random_weighs()
                    print("Веса сброшены")
                if l3 == 3:
                    print("Повторение обучения")
                    train(epoch)

        if l2 == 2:
            print(
                "Введите ключевые слова через запятую с пробелами в одну строку. Например: нейронная сеть, информатика, ...")
            list_str = str(input()).split(",")
            str = []
            for i in range(count_inputs):
                if (i < len(list_str)):
                    str.append(get_ASCII_fron_str(list_str[i]))
                else:
                    str.append('0')
            y, out = go_forward(str)
            print(y)

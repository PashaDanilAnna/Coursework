import numpy as np
import random as rand
import io
import chardet
import os
import codecs

import json as json

def f(x):
    return 2/(1+np.exp(-x)) - 1

def df(x):
    return 0.5*(1 + x)*(1 - x)


W = []
outs = []
count_inputs = 3
count_neuron_in_layers = np.array([2, 2, 2, 1])
count_layers = len(count_neuron_in_layers)

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

def random_weighs():
    global W
    W = [] 
    prew_count_neuron_layer = count_inputs
    for i in range(len(count_neuron_in_layers)):
        W1 = []
        for j in range(count_neuron_in_layers[i]):
            W2 = []
            for k in range(prew_count_neuron_layer):
                W2.append(float(rand.uniform(-0.5,0.5)))   
            W1.append(W2) 
        W.append(W1) 
        outs.append([])  
        prew_count_neuron_layer = count_neuron_in_layers[i] 
        
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

def load_data():
    filename = 'train_data.txt' 

    bytes = min(32, os.path.getsize(filename))
    raw = open(filename, 'rb').read(bytes) 

    if raw.startswith(codecs.BOM_UTF8): 
        encoding = 'utf-8-sig'
    else:
        result = chardet.detect(raw)
        encoding = result['encoding']

    infile = io.open(filename, 'r', encoding=encoding) 
    data = infile.read() 
    infile.close() 

    one_line = data.split('\n') 
    for i in range(len(one_line)):
        epoch.append([])
        two_line = one_line[i].split(', ')
        for j in range(count_inputs):
            if (j < len(two_line)-1):
                epoch[i].append(two_line[j])
            else:
                epoch[i].append('0')
        epoch[i].append(float('0.' + two_line[-1].replace('.','')))

    # преобразовать слово в число
    for i in range(len(epoch)):
        for j in range(count_inputs):
            epoch[i][j] = float(get_ASCII_from_str(epoch[i][j]))

def get_ASCII_fron_str(str):
    return sum(list(str.encode('utf-8')))

def get_array_ASCII_from_str(str):
    array_str = []
    for i in range(len(str)):
        array_str.append(get_ASCII_fron_str(str[i]))
    return array_str

def go_forward(inp):
    sum = np.dot(W[0], inp)
    #out = np.array([f(x) for x in sum])
    outs[0] = np.array([f(x) for x in sum])

    # центральные
    for i in range(1,count_layers - 1):
        sum = np.dot(W[i],outs[i-1])
        outs[i] = np.array([f(x) for x in sum])

    sum = np.dot(W[count_layers-1], outs[count_layers-2])
    y = f(sum)
    return (y, outs)

def p_l(delta):
    if len(delta) == 1:
        return delta[0]
    else:
        return delta
    
def train(epoch):
    #global W2, W1
    global W
    lmd = 0.01      # шаг обучения
    N = 0       # число итераций при обучении
    while N < 1 or N > 10000000:
        N = int(input("Введите количество итераций: "))
    count = len(epoch)
    for z in range(N):
        if z % 10000 == 0:
           print("Прошло " + str(z) + " итераций из " + str(N))
        x = epoch[np.random.randint(0,count)]   # случайный выбор входного сигнала из обучающей выборки
        y, outs = go_forward(x[0:count_inputs])             # прямой проход по НС и вычисление выходных значений нейронов
        e = y - x[-1]                           # ошибка
        temp = e*df(y)                         # локальный градиент
        delta = temp[0]
        for j in range(len(W[count_layers-1])):
            W[count_layers-1][j] = W[count_layers-1][j] - lmd * delta * outs[count_layers-2][j]

        # центральный
        delta2 = delta
        for i in range(count_layers-2,0,-1):
            delta3 = []
            if not isinstance(delta2, float):
                for j in range(len(W[i-1])):
                    temp = 0
                    delta3.append([])
                    for k in range(len(W[i])):
                        temp = delta2[k] * W[i][k][j] + temp
                    delta3[j] = temp * df(outs[i-1][j])
            else:
                delta3 = p_l(W[i+1]) * delta2 * df(outs[i])
            delta2 = p_l(delta3)

            for j in range(len(W[i])):
                for k in range(len(W[i][j])):
                    W[i][j][k] = W[i][j][k] - lmd * delta2[j] * outs[i-1][j]    # корректировка веса j связи i слоя

        delta3 = []
        for j in range(len(W[0])):
            temp = 0
            delta3.append([])
            for k in range(len(W[1])):
                temp = delta2[k] * W[1][k][j] + temp
            delta3[j] = temp * df(outs[0][j])
        delta2 = p_l(delta3)

        # корректировка связей первого слоя
        for j in range(len(W[0])):
            for k in range(len(W[0][j])):
                summa = np.sum(x[0:3])
                W[0][j][k] = W[0][j][k] - summa * delta2[j] * lmd

epoch = []

    
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

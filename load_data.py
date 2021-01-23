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
            epoch[i][j] = float(get_ASCII_fron_str(epoch[i][j]))

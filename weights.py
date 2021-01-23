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

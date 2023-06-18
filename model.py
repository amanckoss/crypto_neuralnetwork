import random

import tensorflow as tf
import numpy as np
import time

from db_api import get_orders


def fitness_function(outputs, inputs, param=0.9):
    res = 0
    count = 0

    for i in range(len(outputs)):
        if outputs[i] > param:
            count += 1
            res += inputs[i]
    return res, count


def generate_model() -> tf.keras.Sequential:
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(5, input_shape=(5,), activation='relu'),
        tf.keras.layers.Dense(5, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    # model.build((None, 50))
    return model


def mutation(model, mutation_rate=0.1):
    return generate_model()
    new_model = tf.keras.models.clone_model(model)
    new_model.set_weights(model.get_weights())

    for layer in new_model.layers:
        if layer.get_weights():
            weights = layer.get_weights()[0]
            biases = layer.get_weights()[1]

            mask = np.random.choice([0, 1], size=weights.shape, p=[1 - mutation_rate, mutation_rate])
            mutated_weights = weights * mask
            mutated_biases = biases * mask

            layer.set_weights([mutated_weights, mutated_biases])

    return new_model


def model_work():
    prev_model = generate_model()
    prev_fitness = 0
    model = mutation(prev_model)

    while True:
        input = get_orders()[:5]

        float_input = [float(element) for element in input]

        outputs = model.predict([float_input])[0]

        fitness, count_promotion = fitness_function(outputs, float_input)

        print("test fitness", fitness)
        print("max fitness", prev_fitness)

        # buy_promotion(count_promotion)

        if fitness > prev_fitness:
            prev_model = model
            prev_fitness = fitness

        model = mutation(prev_model)


        time.sleep(1)

model_work()
# m = generate_model()
# mutate_model(m, 0.1)
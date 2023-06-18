import random

import tensorflow as tf
import numpy as np
import time

from main import getCrypto

# def getCrypto():
#     random_numbers = []
#     for _ in range(50):
#         random_numbers.append(random.randint(1, 10))  # Adjust the range as per your requirements
#     return random_numbers


def fitness_function(outputs: list, inputs: list, param=0.9):
    res = 0
    count = 0
    for o, i in zip(outputs, inputs):
        if o > param:
            count += 1
            res += i
    return res, count


def generate_model() -> tf.keras.Sequential:
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(50, activation='relu'),
        tf.keras.layers.Dense(50, activation='relu'),
        tf.keras.layers.Dense(50, activation='sigmoid')
    ])
    model.build((None, 50))
    return model


def mutation(model, mutation_rate=0.1):
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
        input = getCrypto()

        outputs = model.predict(np.expand_dims(input, axis=0))[0]
        fitness, count_promotion = fitness_function(outputs, input)

        print(fitness, " ", count_promotion)

        # buy_promotion(count_promotion)

        if fitness > prev_fitness:
            prev_model = model

        model = mutation(prev_model)
        prev_fitness = fitness

        time.sleep(6)

model_work()
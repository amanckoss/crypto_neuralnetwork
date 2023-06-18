import random

import tensorflow as tf
import numpy as np
import time

from db_api import get_orders, close_order


def fitness_function(outputs, float_input_buy, float_input_sell, param=0.9):
    res = 500-abs(500-outputs)
    count = 0

    for i in float_input_buy:
        if i < outputs*param:
            close_order(i, 'buy')
            break
    for i in float_input_sell:
        if i > outputs/param:
            close_order(i, 'sell')
            break

    return res, count


def generate_model() -> tf.keras.Sequential:
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(20, input_shape=(200,), activation='relu'),
        tf.keras.layers.Dense(1, activation='relu')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model


def mutation(model, mutation_rate=0.005):
    new_model = tf.keras.models.clone_model(model)
    old_weights = model.get_weights()

    def add_random_values(arr):
        if isinstance(arr, float):
            return arr + np.random.uniform(-mutation_rate, mutation_rate)
        elif isinstance(arr, np.ndarray):
            return arr + np.random.uniform(-mutation_rate, mutation_rate, arr.shape)
        else:
            return arr

    new_weights = [add_random_values(weight) for weight in old_weights]
    new_model.set_weights(new_weights)
    return new_model


def model_work():
    prev_model = generate_model()
    prev_fitness = 0
    model = mutation(prev_model)

    while True:
        input_buy = get_orders('buy')
        input_sell = get_orders('sell')

        float_input_buy = [float(element) for element in input_buy]
        float_input_sell = [float(element) for element in input_sell]
        float_input = []
        float_input.extend(float_input_buy)
        float_input.extend(float_input_sell)

        output = model.predict([float_input])[0][0]
        print(output)

        fitness, count_promotion = fitness_function(output, float_input_buy, float_input_sell)


        print("test fitness", fitness, " ", count_promotion)
        print("max fitness", prev_fitness)

        # buy_promotion(count_promotion)
        if fitness == 0:
            prev_model = generate_model()
        if fitness >= prev_fitness:
            prev_model = model
            prev_fitness = fitness

        model = mutation(prev_model)


        time.sleep(3)


# m = generate_model()
# mutate_model(m, 0.1)
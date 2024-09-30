# models/immaterial_layers.py

import tensorflow as tf
from tensorflow.keras import layers

# Custom Quantum Layer
class CustomQuantumLayer(tf.keras.layers.Layer):
    def __init__(self, units=2, **kwargs):
        super(CustomQuantumLayer, self).__init__(**kwargs)
        self.units = units

    def build(self, input_shape):
        # Initialize real and imaginary parts for the complex weights
        self.real_kernel = self.add_weight(shape=(input_shape[-1], self.units),
                                           initializer='glorot_uniform',
                                           trainable=True,
                                           dtype=tf.float32)

        self.imaginary_kernel = self.add_weight(shape=(input_shape[-1], self.units),
                                                initializer='glorot_uniform',
                                                trainable=True,
                                                dtype=tf.float32)

    def call(self, inputs):
        # Split the input into real and imaginary parts if needed
        real_part = tf.math.real(inputs)
        imaginary_part = tf.math.imag(inputs)

        # Perform matrix multiplication with the real and imaginary kernels
        real_output = tf.matmul(real_part, self.real_kernel)
        imaginary_output = tf.matmul(imaginary_part, self.imaginary_kernel)

        # Combine the real and imaginary outputs into complex numbers again
        output = tf.complex(real_output, imaginary_output)
        return output

# Build the immaterial model
def build_immaterial_model():
    quantum_input = layers.Input(shape=(2,), dtype=tf.complex64, name="quantum_input")
    
    # Replace the quantum layer with the custom quantum layer
    q_layer = CustomQuantumLayer(units=2, name="custom_quantum_layer")(quantum_input)

    model = tf.keras.Model(inputs=quantum_input, outputs=q_layer)
    return model

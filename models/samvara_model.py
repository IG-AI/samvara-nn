# models/samvara_model.py

import tensorflow as tf
from tensorflow.keras.layers import Input, Dense, Concatenate, Layer
from tensorflow.keras.models import Model
from models.material_layers import build_material_model
from models.immaterial_layers import build_immaterial_model

# Custom layer to handle real part extraction
class RealPartLayer(Layer):
    def call(self, inputs):
        return tf.math.real(inputs)

def build_samvara_model():
    # Material model (image and text inputs)
    image_input = Input(shape=(32, 32, 3), name='image_input')
    text_input = Input(shape=(100,), name='text_input')
    material_model = build_material_model()

    material_output = material_model([image_input, text_input])

    # Immaterial model (quantum input)
    real_input = Input(shape=(2,), name='real_input')
    imaginary_input = Input(shape=(2,), name='imaginary_input')
    immaterial_model = build_immaterial_model()

    immaterial_output = immaterial_model([real_input, imaginary_input])

    # Use a custom layer to extract the real part of the complex immaterial output
    immaterial_output_real = RealPartLayer()(immaterial_output)

    # Concatenate material and immaterial outputs (now both float32)
    combined_output = Concatenate()([material_output, immaterial_output_real])

    # Final dense layers for classification
    output = Dense(10, activation='softmax')(combined_output)

    model = Model(inputs=[image_input, text_input, real_input, imaginary_input], outputs=output)
    return model

# main.py

import os
import numpy as np
import tensorflow as tf
from models.samvara_model import build_samvara_model
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
import h5py
import time

# Set random seed for reproducibility
np.random.seed(42)
tf.random.set_seed(42)

# Hyperparameters
BATCH_SIZE = 32
EPOCHS = 50
LEARNING_RATE = 0.001

# Data Augmentation for Image Data
data_augmentation = tf.keras.preprocessing.image.ImageDataGenerator(
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True
)

# Efficient data handling (dummy data for example purposes)
def load_data():
    num_samples = 1000
    image_data = np.random.random((num_samples, 32, 32, 3))
    text_data = np.random.randint(10000, size=(num_samples, 100))
    quantum_data = np.random.random((num_samples, 2))
    labels = np.random.randint(10, size=(num_samples, 10))  # Assuming 10 classes
    return image_data, text_data, quantum_data, labels

# Load data
image_data, text_data, quantum_data, labels = load_data()

# Augment the image data
train_data_gen = data_augmentation.flow(image_data, labels, batch_size=BATCH_SIZE)

# Build the Samvara model
model = build_samvara_model()

# Compile the model with a lower learning rate for better optimization
optimizer = tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE)
model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])

# Create a directory for saving models if it doesn't exist
checkpoint_dir = "checkpoints/"
if not os.path.exists(checkpoint_dir):
    os.makedirs(checkpoint_dir)

# Function to delete previous checkpoints
def clear_existing_checkpoints(checkpoint_dir):
    for file in os.listdir(checkpoint_dir):
        if file.endswith(".h5"):
            os.remove(os.path.join(checkpoint_dir, file))

# Clear any previous checkpoints
clear_existing_checkpoints(checkpoint_dir)

# Create a unique filename for checkpoints using timestamp
def generate_unique_filename(base_name='best_model'):
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    return f"{checkpoint_dir}/{base_name}_{timestamp}.h5"

# Model Checkpoint: Save the best model during training with unique filenames
checkpoint_path = generate_unique_filename()

checkpoint = ModelCheckpoint(
    filepath=checkpoint_path,
    save_best_only=True,
    monitor='val_loss',
    verbose=1,
    save_weights_only=True  # Save only weights
)

# Early Stopping: Stop training if validation loss doesn't improve after 5 epochs
early_stopping = EarlyStopping(
    monitor='val_loss',
    patience=5,
    restore_best_weights=True,
    verbose=1
)

# Print the model summary to inspect the layers
model.summary()

# Train the model with unique checkpoint filenames
history = model.fit(
    [image_data, text_data, quantum_data],
    labels,
    validation_split=0.2,  # Use 20% of the data for validation
    epochs=EPOCHS,
    batch_size=BATCH_SIZE,
    callbacks=[checkpoint, early_stopping],
    verbose=1
)

# Manually save the model's weights after training
final_weights_path = f"{checkpoint_dir}/final_model_weights.h5"
model.save_weights(final_weights_path)
print(f"Weights saved to {final_weights_path}")

# Manually save the entire model after training
final_model_path = f"{checkpoint_dir}/final_model"
model.save(final_model_path)
print(f"Model saved to {final_model_path}")

# Evaluate the model
loss, accuracy = model.evaluate([image_data, text_data, quantum_data], labels)
print(f"Final Loss: {loss}, Final Accuracy: {accuracy}")

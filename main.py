import numpy as np
import tensorflow as tf
from samvara_model import build_samvara_model
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
import os

# Set random seed for reproducibility
np.random.seed(42)
tf.random.set_seed(42)

# Hyperparameters
BATCH_SIZE = 32
EPOCHS = 50
LEARNING_RATE = 0.001
CHECKPOINT_PATH = 'best_model.h5'  # Path to the checkpoint file

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

# Build the Samvara model
model = build_samvara_model()

# Compile the model with a lower learning rate for better optimization
optimizer = tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE)
model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])

# Check if a checkpoint exists and load it
if os.path.exists(CHECKPOINT_PATH):
    print("Loading the last checkpoint to resume training...")
    model.load_weights(CHECKPOINT_PATH)

# Model Checkpoint: Save the best model during training
checkpoint = ModelCheckpoint(
    filepath=CHECKPOINT_PATH,
    save_best_only=True,
    monitor='val_loss',
    verbose=1
)

# Early Stopping: Stop training if validation loss doesn't improve after 5 epochs
early_stopping = EarlyStopping(
    monitor='val_loss',
    patience=5,
    restore_best_weights=True,
    verbose=1
)

# Train the model (continue from checkpoint if loaded)
history = model.fit(
    [image_data, text_data, quantum_data],
    labels,
    validation_split=0.2,
    epochs=EPOCHS,
    batch_size=BATCH_SIZE,
    callbacks=[checkpoint, early_stopping],
    verbose=1
)

# Evaluate the model
loss, accuracy = model.evaluate([image_data, text_data, quantum_data], labels)
print(f"Final Loss: {loss}, Final Accuracy: {accuracy}")

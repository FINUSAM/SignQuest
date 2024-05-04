print('\nimporting required libraries')
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress TensorFlow GPU warnings
import cv2
from keras.applications import MobileNetV2
from keras.layers import Dropout, Dense, GlobalAveragePooling2D
from keras.models import Model
import numpy as np
from tensorflow.keras.utils import to_categorical
print('libraries imported successfully')

print('\nDefining variables and functions')

# Define dataset paths and image size
dataset_paths = ['retrain_data']
image_size = 224

# Define label list and map labels to integers
label_lst = ['A', 'Aa', 'E']
NUM_CLASSES = len(label_lst)
CLASS_MAP = {label_lst[i]: i for i in range(NUM_CLASSES)}

# Mapper function to map labels to integers
def mapper(val):
    return CLASS_MAP[val]

# Function to load dataset images and labels
def load_dataset(dataset_paths, image_size):
    dataset = []
    for dataset_path in dataset_paths:
        for directory in os.listdir(dataset_path):
            path = os.path.join(dataset_path, directory)
            if not os.path.isdir(path):
                continue
            for item in os.listdir(path):
                if item.startswith("."):
                    continue
                if not item.endswith(".jpg"):
                    continue
                img = cv2.imread(os.path.join(path, item))
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img = cv2.resize(img, (image_size, image_size))
                dataset.append([img, directory])
    return dataset

print('functions and variables defined successfully')

# Load dataset images and labels
print('\nLoading dataset')
dataset = load_dataset(dataset_paths, image_size)
print('dataset loaded successfully')

# Separate images and labels
data, labels = zip(*dataset)

# Map labels to integers and one-hot encode them
labels = list(map(mapper, labels))
labels = to_categorical(labels, num_classes=NUM_CLASSES)

# Load pre-trained MobileNetV2 model
print("\nLoading pre-trained MobileNetV2 model...")
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(image_size, image_size, 3))
print("MobileNetV2 model loaded.")

# Freeze convolutional layers of MobileNetV2
for layer in base_model.layers:
    layer.trainable = False

# Add custom top layers for classification
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dropout(0.5)(x)
x = Dense(512, activation='relu')(x)  # Add additional dense layer for better feature representation
predictions = Dense(NUM_CLASSES, activation='softmax')(x)

# Create the model
model = Model(inputs=base_model.input, outputs=predictions)

# Compile model
print("\nCompiling the model...")
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
print("Model compiled successfully.")

from keras.callbacks import EarlyStopping

# Define early stopping criteria
early_stopping = EarlyStopping(monitor='val_loss', patience=3, verbose=1, mode='auto')

# Start training
print("\nTraining the model...")
model.fit(np.array(data), np.array(labels), epochs=50, validation_split=0.2, callbacks=[early_stopping])
print("Training completed.")

# Save the model for later use
print("\nSaving the model...")
model.save('retrained_model_AAaE_only_with_early_stopping.keras')
print("Model saved successfully.")

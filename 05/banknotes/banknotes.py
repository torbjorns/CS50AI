import csv
import tensorflow as tf
import numpy as np

import os
print("CUDA_HOME:", os.environ.get("CUDA_HOME"))
print("PATH:", os.environ.get("PATH"))

print("GPUs Available: ", tf.config.list_physical_devices('GPU'))

from sklearn.model_selection import train_test_split

# Read data in from file
with open("banknotes.csv") as f:
    reader = csv.reader(f)
    next(reader)

    data = []
    for row in reader:
        data.append({
            "evidence": [float(cell) for cell in row[:4]],
            "label": 1 if row[4] == "0" else 0
        })

# Separate data into training and testing groups
evidence = [row["evidence"] for row in data]
labels = [row["label"] for row in data]
X_training, X_testing, y_training, y_testing = train_test_split(
    evidence, labels, test_size=0.4
)

# Create a sequential model with an Input layer first
model = tf.keras.models.Sequential([
    # Start with an Input layer to define the shape of input data
    tf.keras.layers.Input(shape=(4,)),
    
    # Then add a hidden layer with 8 units and ReLU activation
    tf.keras.layers.Dense(8, activation="relu"),
    
    # Add output layer with 1 unit, with sigmoid activation
    tf.keras.layers.Dense(1, activation="sigmoid")
])

# Use Adam optimizer
# Binary crossentropy is used for binary classification in the loss function
# Accuracy is chosen as metric
model.compile(
    optimizer="adam",                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

# Fit model on training data
X_training = np.array(X_training)
y_training = np.array(y_training)
model.fit(X_training, y_training, epochs=20)

# Evaluate how well model performs
X_testing = np.array(X_testing)
y_testing = np.array(y_testing)
model.evaluate(X_testing, y_testing, verbose=2)

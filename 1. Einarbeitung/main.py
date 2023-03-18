'''
Kernel Ridge Regression Modell mit dem Fuel Effiency Dataset mit Tensorflow und Tensorflow Keras Regression Tutorial.
Training auf die Verbrauch, anhand von Motenrenwerten.
'''

import tensorflow as tf
import tensorflow_probability as tfp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras import layers
from tensorflow.keras.layers.experimental import preprocessing

__author__ = "Tjark Prokoph, Niclas Zeiss"

# Funktionen
def plot_history(history):
    plt.plot(history.history['loss'], label='loss')
    plt.plot(history.history['val_loss'], label='val_loss')
    plt.ylim([0, 10])
    plt.xlabel('Epoch')
    plt.ylabel('Error')
    plt.legend()
    plt.grid(True)

def plot_predictions(labels, predictions):
    plt.axes(aspect='equal')
    plt.scatter(labels, predictions)
    plt.xlabel('True Values')
    plt.ylabel('Predictions')
    lims = [0, 50]
    plt.xlim(lims)
    plt.ylim(lims)
    plt.plot(lims, lims)
    plt.grid(True)

# Numpy Einstellungen
np.set_printoptions(precision=3, suppress=True)

# Download des Dataset und auslesen aus der CSV-Datei
url = 'http://archive.ics.uci.edu/ml/machine-learning-databases/auto-mpg/auto-mpg.data'
column_names = ['MPG', 'Cylinders', 'Displacement', 'Horsepower', 'Weight',
                'Acceleration', 'Model Year', 'Origin']
dataset = pd.read_csv(url, names=column_names, na_values='?', comment='\t', sep=' ', skipinitialspace=True)
dataset = dataset.dropna()
dataset['Origin'] = dataset['Origin'].map({1: 'USA', 2: 'Europe', 3: 'Japan'})
dataset = pd.get_dummies(dataset, prefix='', prefix_sep='')

# Aufteilen der Datensätze in Trainingsdaten und Testdaten
train_dataset = dataset.sample(frac=0.8, random_state=0)
test_dataset = dataset.drop(train_dataset.index)

# Teilen der Features vom Label
train_features = train_dataset.copy()
test_features = test_dataset.copy()
train_labels = train_features.pop('MPG')
test_labels = test_features.pop('MPG')

# Normalisierungsebene erstellen ohne festen Input-Shape
normalizer = preprocessing.Normalization()
normalizer.adapt(np.array(train_features))

# KRR Modell erstellen und auf einen Ausgang einstellen
linear_model = tf.keras.Sequential([
    normalizer,
    layers.Dense(units=1, kernel_regularizer="l2")
])

# KRR Modell kompilieren
linear_model.compile(
    optimizer=tf.optimizers.Adam(learning_rate=0.1),
    loss='mean_absolute_error',
    metrics=[tf.keras.metrics.Accuracy()])

# KRR Modell trainieren
history = linear_model.fit(
    train_features, train_labels,
    epochs=100,
    verbose=2,
    batch_size= 20,
    validation_split = 0.2)

# Trainingserfolg ausgeben
plot_history(history)
plt.show()

# Testerfolg des KRR Modells ausgeben
test_predictions = linear_model.predict(test_features).flatten()
plot_predictions(test_labels, test_predictions)
plt.show()
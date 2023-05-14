# Load the data and split it between train and test sets
from keras.datasets import mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# Scale images to the [0, 1] range
x_train = x_train / 255
x_test = x_test / 255 

# Apply one-hot encoding
from keras.utils.np_utils import to_categorical
y_train = to_categorical(y_train, 10)
y_test = to_categorical(y_test, 10)

# Create the model
from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPool2D, Flatten, BatchNormalization, Dropout

model = Sequential()

model.add(Conv2D(filters=32, kernel_size=(3, 3), input_shape=(28, 28, 1), activation="relu"))
model.add(BatchNormalization())
model.add(Conv2D(filters=64, kernel_size=(3, 3),  activation="relu"))
model.add(BatchNormalization())
model.add(MaxPool2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(filters=128, kernel_size=(3, 3),  activation="relu"))
model.add(BatchNormalization())
model.add(Conv2D(filters=256, kernel_size=(3, 3),  activation="relu"))
model.add(BatchNormalization())
model.add(MaxPool2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(512, activation='relu'))
model.add(BatchNormalization())
model.add(Dropout(0.25))
model.add(Dense(1024, activation='relu'))
model.add(BatchNormalization())
model.add(Dropout(0.5))
model.add(Dense(10, activation='softmax'))

model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

# Expand the dataset artificially to prevent overfitting.
x_train = x_train.reshape(len(x_train), 28, 28, 1)
x_test = x_test.reshape(len(x_test), 28, 28, 1)

from keras.preprocessing.image import ImageDataGenerator
datagen = ImageDataGenerator(rotation_range=15, zoom_range = 0.1, width_shift_range=0.1, height_shift_range=0.1)

train_gen = datagen.flow(x_train, y_train, batch_size=16)
test_gen = datagen.flow(x_test, y_test, batch_size=16)

# Train the model
model.fit(train_gen, epochs=10)

# Evaluate the model (accuracy: 0.9904)
model.evaluate(test_gen)

# Save the model
model.save("model.h5") 
#import os
#os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"

# CNN imports 
from keras import layers
from keras.models import Sequential
from keras.preprocessing.image import ImageDataGenerator

# Start of the model 
model = Sequential()

# first convolutional layer 
model.add(layers.Conv2D(filters = 32, kernel_size = (3,3) , input_shape = (64,64,3),
                        strides = (1,1), activation = 'relu'))

# max pooling 
model.add(layers.MaxPooling2D(pool_size = (2,2), strides = (2,2)))

# second covlolution layer 
model.add(layers.Conv2D(filters = 64, kernel_size = (3,3) ,
                        strides = (1,1), activation = 'relu'))

model.add(layers.MaxPooling2D(pool_size = (2,2), strides = (2,2)))


# flatten 
model.add(layers.Flatten())

# input layer to Neural Network 
model.add(layers.Dense(units = 128, activation = 'relu',))

# hidden layer 
model.add(layers.Dense(units = 32, activation = 'relu',))

# 50% dropout rate 
model.add(layers.Dropout(0.5))

# output layer -> softmax output prob 0 - 1
model.add(layers.Dense(units = 1, activation = 'sigmoid',))

# compile the model ;;; adam = optimizer, loss = cost function
model.compile(optimizer='adam', loss='binary_crossentropy', metrics = ['accuracy'])

# load and augment the data 
train_data = ImageDataGenerator(rescale = 1./255,
                                   shear_range = 0.2,
                                   zoom_range = 0.2,
                                   horizontal_flip = True)

test_data = ImageDataGenerator(rescale = 1./255)

training_set = train_data.flow_from_directory('/Users/benjaminkolber/Desktop/CNN_cats_and_dogs/training_set',
                                                 target_size = (64, 64),
                                                 batch_size = 32,
                                                 class_mode = 'binary')

test_set = test_data.flow_from_directory('/Users/benjaminkolber/Desktop/CNN_cats_and_dogs/test_set',
                                            target_size = (64, 64),
                                            batch_size = 32,
                                            class_mode = 'binary')

# steps_per_epoch = training set
# epoch = training epochs
# validatoin_data = test data
# validation steps = test data size 
model.fit_generator(training_set,
                         steps_per_epoch = 8000,
                         epochs = 25,
                         verbose = 1,
                         validation_data = test_set,
                         validation_steps = 2000)





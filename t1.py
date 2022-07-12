# import torch
# import torch.nn as nn
# import torch.nn.functional as F

# # class Net(nn.Module):

# #     def __init__(self):
# #         super(Net, self).__init__()
# #         # 1 input image channel, 6 output channels, 5x5 square convolution
# #         # kernel
# #         self.conv1 = nn.Conv2d(1, 6, 5)
# #         self.conv2 = nn.Conv2d(6, 16, 5)
# #         # an affine operation: y = Wx + b
# #         self.fc1 = nn.Linear(16 * 5 * 5, 120)  # 5*5 from image dimension
# #         self.fc2 = nn.Linear(120, 84)
# #         self.fc3 = nn.Linear(84, 10)

# #     def forward(self, x):
# #         # Max pooling over a (2, 2) window
# #         x = F.max_pool2d(F.relu(self.conv1(x)), (2, 2))
# #         # If the size is a square, you can specify with a single number
# #         x = F.max_pool2d(F.relu(self.conv2(x)), 2)
# #         x = torch.flatten(x, 1) # flatten all dimensions except the batch dimension
# #         x = F.relu(self.fc1(x))
# #         x = F.relu(self.fc2(x))
# #         x = self.fc3(x)
# #         return x

# model = nn.Sequential(nn.Linear(2, 3),
#                       nn.ReLU(),
#                       nn.Linear(3, 1),
#                       nn.Sigmoid())


# # MSE_loss_fn = nn.MSELoss()
# # from t2 import A
# # a = A(torch.Tensor([[1,2,3],[4,5,6]]),torch.Tensor([[1,2,3],[4,5,6]]),MSE_loss_fn)
# # print(a.bla())
# input = torch.randn(2)
# output = torch.Tensor([0.2131231])

# import pickle 
# pickle.dump(input, open("input.pkl", "wb"))
# pickle.dump(output, open("output.pkl", "wb"))
# # print(output)
# # print(output1)
# # print(input)
# m = torch.jit.script(model)

# torch.jit.save(m, '1.pt')

# # import tensorflow as tf
# # import numpy as np
# # import matplotlib.pyplot as plt
# # from tensorflow.keras.layers import Input, Conv2D, Dense, Flatten, Dropout
# # from tensorflow.keras.layers import GlobalMaxPooling2D, MaxPooling2D
# # from tensorflow.keras.layers import BatchNormalization
# # from tensorflow.keras.models import Model
# # from tensorflow.keras.models import load_model

# # # number of classes
# # K = 3
# # # calculate total number of classes for output layer
# # print("number of classes:", K)

# # # Build the model using the functional API
# # # input layer
# # i = Input(shape=(28, 28, 1))
# # x = Conv2D(32, (3, 3), activation='relu', padding='same')(i)
# # x = BatchNormalization()(x)
# # x = Conv2D(32, (3, 3), activation='relu', padding='same')(x)
# # x = BatchNormalization()(x)
# # x = MaxPooling2D((2, 2))(x)

# # x = Conv2D(64, (3, 3), activation='relu', padding='same')(x)
# # x = BatchNormalization()(x)
# # x = Conv2D(64, (3, 3), activation='relu', padding='same')(x)
# # x = BatchNormalization()(x)
# # x = MaxPooling2D((2, 2))(x)

# # x = Conv2D(128, (3, 3), activation='relu', padding='same')(x)
# # x = BatchNormalization()(x)
# # x = Conv2D(128, (3, 3), activation='relu', padding='same')(x)
# # x = BatchNormalization()(x)
# # x = MaxPooling2D((2, 2))(x)

# # x = Flatten()(x)
# # x = Dropout(0.2)(x)

# # # Hidden layer
# # x = Dense(1024, activation='relu')(x)
# # x = Dropout(0.2)(x)

# # # last hidden layer i.e.. output layer
# # x = Dense(K, activation='softmax')(x)

# # model = Model(i, x)
# # model.summary()

# # model.save('gfgModel.h5')
# # print('Model Saved!')

# # from sklearn import svm
# # from sklearn import datasets

# # iris = datasets.load_iris()
# # X, y = iris.data, iris.target

# # clf = svm.SVC()
# # clf.fit(X, y)  

# # ##########################
# # # SAVE-LOAD using joblib #
# # ##########################
# # import joblib

# # # save
# # joblib.dump(clf, "model.pkl") 

# # from tensorflow import keras
# # import tensorflow as tf
# # from tensorflow.keras import layers
# # import numpy as np

# # input_dim = (28, 28)
# # # get output dimensions 10 classes
# # output_dim = 3

# # # create sequential model
# # model = keras.Sequential()
# # model.add(layers.Flatten(input_shape=input_dim))
# # model.add(layers.Dense(units=128, activation='relu'))
# # model.add(layers.BatchNormalization())
# # model.add(layers.Dense(units=128, activation='relu'))
# # model.add(layers.BatchNormalization())
# # model.add(layers.Dense(units=output_dim))


# # model.save('gfgModel.h5')
# #random keras tensor with above shapes




# #random tensorflow tensor with above shapes

# # output = model(np.random.rand(1,28, 28))
# # output = tf.constant([[0.770061,0.46085632,0.12955794]], dtype=tf.float32)
# # import pickle 
# # input = np.random.rand(1,28, 28)


# # pickle.dump(input, open("input.pkl", "wb"))

import time
import datetime
#print current time in hour format and print current time after 2 hours
a = datetime.datetime.now()
print(a.strftime("%H:%M:%S"))

time.sleep(65)
b = datetime.datetime.now()
print(b.strftime("%H:%M:%S"))
c = b-a
print(c.seconds)
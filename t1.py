# import torch
# import torch.nn as nn
# import torch.nn.functional as F

# class Net(nn.Module):

#     def __init__(self):
#         super(Net, self).__init__()
#         # 1 input image channel, 6 output channels, 5x5 square convolution
#         # kernel
#         self.conv1 = nn.Conv2d(1, 6, 5)
#         self.conv2 = nn.Conv2d(6, 16, 5)
#         # an affine operation: y = Wx + b
#         self.fc1 = nn.Linear(16 * 5 * 5, 120)  # 5*5 from image dimension
#         self.fc2 = nn.Linear(120, 84)
#         self.fc3 = nn.Linear(84, 10)

#     def forward(self, x):
#         # Max pooling over a (2, 2) window
#         x = F.max_pool2d(F.relu(self.conv1(x)), (2, 2))
#         # If the size is a square, you can specify with a single number
#         x = F.max_pool2d(F.relu(self.conv2(x)), 2)
#         x = torch.flatten(x, 1) # flatten all dimensions except the batch dimension
#         x = F.relu(self.fc1(x))
#         x = F.relu(self.fc2(x))
#         x = self.fc3(x)
#         return x

# m = torch.jit.script(Net())

# # Save to file
# torch.jit.save(m, 'scriptmodule.pt')

# import tensorflow as tf
# import numpy as np
# import matplotlib.pyplot as plt
# from tensorflow.keras.layers import Input, Conv2D, Dense, Flatten, Dropout
# from tensorflow.keras.layers import GlobalMaxPooling2D, MaxPooling2D
# from tensorflow.keras.layers import BatchNormalization
# from tensorflow.keras.models import Model
# from tensorflow.keras.models import load_model

# # number of classes
# K = 3
# # calculate total number of classes for output layer
# print("number of classes:", K)

# # Build the model using the functional API
# # input layer
# i = Input(shape=(28, 28, 1))
# x = Conv2D(32, (3, 3), activation='relu', padding='same')(i)
# x = BatchNormalization()(x)
# x = Conv2D(32, (3, 3), activation='relu', padding='same')(x)
# x = BatchNormalization()(x)
# x = MaxPooling2D((2, 2))(x)

# x = Conv2D(64, (3, 3), activation='relu', padding='same')(x)
# x = BatchNormalization()(x)
# x = Conv2D(64, (3, 3), activation='relu', padding='same')(x)
# x = BatchNormalization()(x)
# x = MaxPooling2D((2, 2))(x)

# x = Conv2D(128, (3, 3), activation='relu', padding='same')(x)
# x = BatchNormalization()(x)
# x = Conv2D(128, (3, 3), activation='relu', padding='same')(x)
# x = BatchNormalization()(x)
# x = MaxPooling2D((2, 2))(x)

# x = Flatten()(x)
# x = Dropout(0.2)(x)

# # Hidden layer
# x = Dense(1024, activation='relu')(x)
# x = Dropout(0.2)(x)

# # last hidden layer i.e.. output layer
# x = Dense(K, activation='softmax')(x)

# model = Model(i, x)
# model.summary()

# model.save('gfgModel.h5')
# print('Model Saved!')

from sklearn import svm
from sklearn import datasets

iris = datasets.load_iris()
X, y = iris.data, iris.target

clf = svm.SVC()
clf.fit(X, y)  

##########################
# SAVE-LOAD using joblib #
##########################
import joblib

# save
joblib.dump(clf, "model.pkl") 

from Core1.app import App
import torch.nn as nn
import tensorflow as tf
optimizer = tf.keras.optimizers.SGD(learning_rate=1.7)
#Tensorflow mse loss function
loss = tf.keras.losses.MSE
app = App('Core1/conf.yml',loss,optimizer)
app.run()

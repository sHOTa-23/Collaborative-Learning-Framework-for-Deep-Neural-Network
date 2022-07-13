from Core.app_servers import AppServer
import torch.nn as nn
import tensorflow as tf
optimizer = tf.keras.optimizers.SGD(learning_rate=1.7)
#Tensorflow mse loss function
loss = tf.keras.losses.MSE
app = AppServer('Core/conf.yml',loss,optimizer)
app.run()

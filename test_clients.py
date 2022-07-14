from Core.app_clients import AppClient
import torch.nn as nn
# import tensorflow as tf
# tf.autograph.set_verbosity(1)
# tf.get_logger().setLevel('INFO')
# optimizer = tf.keras.optimizers.SGD(learning_rate=1.7)
# #Tensorflow mse loss function
# loss = tf.keras.losses.MSE
loss = nn.MSELoss()
app = AppClient('Core/conf.yml',loss)
app.run()


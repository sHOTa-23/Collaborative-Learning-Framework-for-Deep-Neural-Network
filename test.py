from Core.app import App
import torch.nn as nn
# import tensorflow as tf
# optimizer = tf.keras.optimizers.SGD(learning_rate=1.7)
app = App('Core/conf.yml',nn.MSELoss())
app.run()
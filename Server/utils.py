from io import BytesIO
import logging
import pickle
from os.path import exists
logging.basicConfig(level=logging.NOTSET)
def prepare_model(model):
    buffer = BytesIO()
    model_type = str(type(model))
    model_parent_type = str(type(model).__bases__)
    if 'keras' in model_type or 'keras' in model_parent_type:
        import tensorflow as tf
        tf.autograph.set_verbosity(1)
        tf.get_logger().setLevel('INFO')
        from tensorflow.keras.models import save_model
        import h5py
        with h5py.File(buffer, 'w') as f:
            save_model(model, f, include_optimizer=True)
    elif 'sklearn' in model_type or 'sklearn' in model_parent_type:
        from joblib import load, dump
        dump(model, buffer)
    elif 'torch' in model_type or 'torch' in model_parent_type:
        import torch
        scripted_model = torch.jit.script(model)
        torch.jit.save(scripted_model, buffer)
    buffer.seek(0)
    logging.debug("Model Prepared")
    return buffer.read()


def load_model(model_type,model_path):
    model = None
    if not exists(model_path):
        return None
    if model_type == "sklearn":
        from joblib import load
        model = load(model_path)
    elif model_type == "tensorflow":
        import tensorflow as tf
        tf.autograph.set_verbosity(1)
        tf.get_logger().setLevel('INFO')
        from tensorflow.keras.models import load_model
        model = load_model(model_path)
    elif model_type == "pytorch":
        import torch
        model = torch.jit.load(model_path)
    logging.info(f"{model_type} Model loaded")  
    return model
    
def save_model(model_type,model_name,model):
    if model_type == 'pytorch':
        import torch
        m = torch.jit.script(model)
        torch.jit.save(m, model_name)
        logging.info("Averaged Model has been saved on Server")
    elif model_type == 'tensorflow':
        import tensorflow as tf
        tf.autograph.set_verbosity(1)
        tf.get_logger().setLevel('INFO')
        from tensorflow.keras.models import save_model
        import h5py
        with h5py.File(model_name, 'w') as f:
            save_model(model, f)
        logging.info("Averaged Model has been saved on Server")

def receive(client_socket,model_type, socket_buffer_size=1024):
    buffer = BytesIO()
    while True:
        data = client_socket.recv(socket_buffer_size)
        if not data:
            break
        buffer.write(data)
        buffer.seek(-4, 2)
        if b'EOF' in buffer.read():
            break
    buffer.seek(0)
    model = load_data(buffer,model_type)
    logging.info("Model Receiving finished")
    return model

def load_data(file: BytesIO,model_type):
    data = file.read()[:-3]
    file.seek(0)
    if model_type == 'sklearn':
        from joblib import load
        return load(file)
    elif model_type == 'tensorflow':
        import tensorflow as tf
        tf.autograph.set_verbosity(1)
        tf.get_logger().setLevel('INFO')
        from tensorflow.keras.models import load_model
        import h5py
        with h5py.File(file, 'r') as f:
            model = load_model(f)
        return model
    elif model_type == 'pytorch':
        import torch
        model = torch.jit.load(file)
        return model

def load_input(input_path,output_path):
    input_data = pickle.load(open(input_path, 'rb'))
    output_data = pickle.load(open(output_path, 'rb'))
    return input_data,output_data
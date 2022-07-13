from io import BytesIO
import logging
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

def receive(client_socket, socket_buffer_size=1024):
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
    
    model = load_data(buffer)
    logging.info("Model Receiving finished")
    return model

def load_data(file: BytesIO):
    data = file.read()[:-3]
    file.seek(0)
    print(file)
    print(b'HDF' in data, b'h5' in data)
    if b'sklearn' in data:
        from joblib import load
        return load(file)
    elif b'HDF' in data or b'h5' in data:
        import tensorflow as tf
        tf.autograph.set_verbosity(1)
        tf.get_logger().setLevel('INFO')
        from tensorflow.keras.models import load_model
        import h5py
        with h5py.File(file, 'r') as f:
            model = load_model(f)
        return model
    elif b'torch' in data:
        import torch
        model = torch.jit.load(file)
        return model


